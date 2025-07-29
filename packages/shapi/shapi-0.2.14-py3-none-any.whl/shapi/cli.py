"""
Command line interface for shapi.
"""

import click
import os
import sys
import signal
from pathlib import Path
from typing import Optional, List, Dict, Any

from rich.console import Console
from rich.table import Table

from .generator import ServiceGenerator
from .core import ShapiService
from .service_manager import ServiceManager, ServiceInfo
import uvicorn


@click.group()
@click.version_option(version="0.2.0")
def main():
    """shapi - Transform shell scripts into production-ready APIs."""
    pass


@main.command()
@click.argument("script_path", type=click.Path(exists=True))
@click.option("--name", "-n", help="Service name (defaults to script filename)")
@click.option("--output", "-o", default="./generated", help="Output directory")
@click.option("--config", "-c", type=click.Path(exists=True), help="Configuration file")
def generate(script_path: str, name: Optional[str], output: str, config: Optional[str]):
    """Generate API service for a shell script."""

    script_path_obj = Path(script_path)
    service_name = name or script_path_obj.stem

    # Load configuration if provided
    service_config = {}
    if config:
        import yaml

        with open(config, "r") as f:
            service_config = yaml.safe_load(f)

    generator = ServiceGenerator(output)
    service_dir = generator.generate_service(script_path, service_name, service_config)

    click.echo(f"✅ Service generated successfully in: {service_dir}")
    click.echo(f"📁 Generated files:")
    click.echo(f"   - main.py")
    click.echo(f"   - Dockerfile")
    click.echo(f"   - Makefile")
    click.echo(f"   - test_service.py")
    click.echo(f"   - requirements.txt")
    click.echo(f"   - docker-compose.yml")
    click.echo(f"   - ansible/test.yml")
    click.echo(f"\n🚀 To run the service:")
    click.echo(f"   cd {service_dir}")
    click.echo(f"   python main.py")


def run_async(coro):
    """Helper to run async functions in sync context."""
    import asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


def print_services_table(services: List[Dict[str, Any]]) -> None:
    """Print a table of running services."""
    if not services:
        Console().print("[yellow]No running services found.[/yellow]")
        return

    table = Table(title="Running shapi Services")
    table.add_column("Name", style="cyan")
    table.add_column("PID", style="green")
    table.add_column("Port", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Uptime", style="blue")
    table.add_column("Script", style="yellow")

    for svc in services:
        status_style = "green" if svc["status"] == "running" else "red"
        table.add_row(
            svc["name"],
            str(svc["pid"]),
            str(svc["port"]),
            f"[{status_style}]{svc['status']}[/{status_style}]",
            svc["uptime"],
            str(svc["script"])
        )

    Console().print(table)

@main.group()
def service():
    """Manage shapi services."""
    pass


@service.command("list")
def list_services():
    """List all running shapi services."""
    manager = ServiceManager()
    services = manager.list_services()
    print_services_table(services)
    return 0


@service.command("stop")
@click.argument("identifier")
@click.option("--force", "-f", is_flag=True, help="Force stop the service")
def stop_service(identifier: str, force: bool):
    """Stop a running shapi service by name or PID."""
    manager = ServiceManager()
    if manager.stop_service(identifier, force):
        click.echo(f"✅ Successfully stopped service: {identifier}")
        return 0
    click.echo(f"❌ Failed to stop service: {identifier}", err=True)
    return 1


@service.command("restart")
@click.argument("identifier")
@click.option("--force", "-f", is_flag=True, help="Force restart the service")
def restart_service(identifier: str, force: bool):
    """Restart a shapi service by name or PID."""
    manager = ServiceManager()
    service, _ = manager.get_service(identifier)
    if not service:
        click.echo(f"❌ Service not found: {identifier}", err=True)
        return 1
    
    # Stop the service
    if not manager.stop_service(identifier, force):
        click.echo(f"❌ Failed to stop service: {identifier}", err=True)
        return 1
    
    # Start the service again
    cmd = [
        sys.executable, "-m", "shapi.cli", "serve",
        str(service.script_path),
        "--name", service.name,
        "--host", service.host,
        "--port", str(service.port)
    ]
    
    try:
        os.execvp(sys.executable, cmd)
    except Exception as e:
        click.echo(f"❌ Failed to restart service: {e}", err=True)
        return 1


@main.command()
@click.argument("script_path", type=click.Path(exists=True))
@click.option("--name", "-n", help="Service name")
@click.option("--host", "-h", default="0.0.0.0", help="Host to bind to")
@click.option("--port", "-p", default=8000, help="Port to bind to")
@click.option("--reload", is_flag=True, help="Enable auto-reload")
@click.option("--force", "-f", is_flag=True, help="Force stop any service running on the same port")
@click.option("--daemon", "-d", is_flag=True, help="Run as a daemon process")
def serve(script_path: str, name: Optional[str], host: str, port: int, reload: bool, force: bool, daemon: bool):
    """Serve a shell script as an API directly."""
    if daemon:
        return _run_as_daemon(script_path, name, host, port, reload, force)
    return _run_serve(script_path, name, host, port, reload, force)


def _run_serve(script_path: str, name: Optional[str], host: str, port: int, reload: bool, force: bool) -> int:
    """Run the serve command in the foreground."""
    import asyncio
    
    async def async_serve():
        try:
            script_path_obj = Path(script_path)
            service_name = name or script_path_obj.stem
            manager = ServiceManager()

            # Create service instance with host and port
            service = ShapiService(script_path, service_name, host=host, port=port)

            # Check if port is available
            is_used, pid = service.is_port_in_use(port, host)
            
            if is_used:
                if not force:
                    click.echo(f"❌ Port {port} is already in use by process {pid}")
                    click.echo(f"   Use --force to stop the existing service")
                    return 1
                
                click.echo(f"⚠️  Stopping existing service on port {port}...")
                if service.stop_process_on_port(port, host):
                    click.echo(f"✅ Successfully stopped process on port {port}")
                    # Small delay to ensure port is released
                    await asyncio.sleep(1)
                else:
                    click.echo(f"❌ Failed to stop process on port {port}")
                    return 1

            # Register the service
            service_info = ServiceInfo(
                name=service_name,
                pid=os.getpid(),
                port=port,
                host=host,
                script_path=str(script_path_obj.absolute())
            )
            manager.register_service(service_info)

            click.echo(f"🚀 Starting shapi service for: {service_name}")
            click.echo(f"📍 Script: {script_path}")
            click.echo(f"🌐 Server: http://{host}:{port}")
            click.echo(f"📖 Docs: http://{host}:{port}/docs")
            click.echo(f"❤️  Health: http://{host}:{port}/health")
            click.echo("🛑 Press Ctrl+C to stop the service")

            # Run the service
            config = uvicorn.Config(
                service.app,
                host=host,
                port=port,
                reload=reload,
                log_level="info"
            )
            server = uvicorn.Server(config)
            
            try:
                await server.serve()
            except asyncio.CancelledError:
                click.echo("\n👋 Shutting down gracefully...")
                await server.shutdown()
            finally:
                manager.unregister_service(os.getpid())
                
        except Exception as e:
            click.echo(f"❌ Error: {str(e)}", err=True)
            return 1
        return 0
    
    # Run the async function in the event loop
    return run_async(async_serve())


def _run_as_daemon(script_path: str, name: Optional[str], host: str, port: int, reload: bool, force: bool) -> int:
    """Run the serve command as a daemon process."""
    import subprocess
    import sys
    
    # Build the command to run in the background
    cmd = [
        sys.executable, "-m", "shapi.cli", "serve",
        script_path,
        "--host", host,
        "--port", str(port),
    ]
    
    if name:
        cmd.extend(["--name", name])
    if reload:
        cmd.append("--reload")
    if force:
        cmd.append("--force")
    
    try:
        # Start the process in the background
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            start_new_session=True
        )
        
        # Wait a bit to check if the process started successfully
        try:
            _, stderr = process.communicate(timeout=2)
            if process.returncode != 0:
                click.echo(f"❌ Failed to start service: {stderr.decode()}", err=True)
                return 1
        except subprocess.TimeoutExpired:
            # If the process is still running after timeout, it probably started successfully
            pass
            
        click.echo(f"✅ Service started in the background (PID: {process.pid})")
        return 0
        
    except Exception as e:
        click.echo(f"❌ Failed to start service: {e}", err=True)
        return 1


@main.command()
@click.argument("service_dir", type=click.Path(exists=True))
def test(service_dir: str):
    """Run tests for generated service."""

    service_path = Path(service_dir)
    test_file = service_path / "test_service.py"

    if not test_file.exists():
        click.echo("❌ Test file not found. Generate service first.")
        sys.exit(1)

    import subprocess

    click.echo("🧪 Running service tests...")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", str(test_file), "-v"], cwd=service_path
    )

    if result.returncode == 0:
        click.echo("✅ All tests passed!")
    else:
        click.echo("❌ Some tests failed.")
        sys.exit(1)


@main.command()
@click.argument("service_dir", type=click.Path(exists=True))
def build(service_dir: str):
    """Build Docker image for generated service."""

    service_path = Path(service_dir)
    dockerfile = service_path / "Dockerfile"

    if not dockerfile.exists():
        click.echo("❌ Dockerfile not found. Generate service first.")
        sys.exit(1)

    import subprocess

    service_name = service_path.name
    image_name = f"shapi-{service_name}:latest"

    click.echo(f"🐳 Building Docker image: {image_name}")

    result = subprocess.run(
        ["docker", "build", "-t", image_name, "."], cwd=service_path
    )

    if result.returncode == 0:
        click.echo(f"✅ Docker image built successfully: {image_name}")
    else:
        click.echo("❌ Docker build failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
