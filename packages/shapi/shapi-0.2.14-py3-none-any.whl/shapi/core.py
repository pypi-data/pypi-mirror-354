"""
Core functionality for shapi service generation and management.
"""

import os
import subprocess
import asyncio
import json
import logging
import socket
import time
import signal
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from dataclasses import dataclass
from enum import Enum

import psutil
from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ScriptStatus(Enum):
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    NOT_FOUND = "not_found"


@dataclass
class ScriptInfo:
    name: str
    path: str
    description: str
    parameters: List[str]
    status: ScriptStatus
    pid: Optional[int] = None


class ScriptRequest(BaseModel):
    parameters: Dict[str, Any] = {}
    async_execution: bool = False


class ScriptResponse(BaseModel):
    status: str
    output: str
    error: Optional[str] = None
    execution_time: float
    pid: Optional[int] = None


class ShapiService:
    """Main service class for managing shell scripts as APIs."""

    def __init__(self, script_path: str, script_name: str, host: str = "0.0.0.0", port: int = 8000):
        self.script_path = Path(script_path)
        self.script_name = script_name
        self.host = host
        self.port = port
        self.app = FastAPI(
            title=f"Shapi Service - {script_name}",
            description=f"API wrapper for {script_name} script",
            version="0.2.0",
        )
        self.running_processes: Dict[str, subprocess.Popen] = {}
        self._stop_event = asyncio.Event()
        self._setup_routes()
        
    @staticmethod
    def is_port_in_use(port: int, host: str = '0.0.0.0') -> Tuple[bool, int]:
        """Check if a port is in use and return the PID of the process using it."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.bind((host, port))
                return False, -1
            except OSError as e:
                if e.errno == 98:  # Port already in use
                    # Try to find the process using the port
                    try:
                        for conn in psutil.net_connections():
                            if conn.status == 'LISTEN' and conn.laddr.port == port:
                                return True, conn.pid
                    except Exception:
                        pass
                return True, -1
    
    @staticmethod
    def stop_process_on_port(port: int, host: str = '0.0.0.0') -> bool:
        """Stop the process running on the specified port."""
        is_used, pid = ShapiService.is_port_in_use(port, host)
        if is_used and pid > 0:
            try:
                os.kill(pid, signal.SIGTERM)
                # Wait for the process to terminate
                for _ in range(10):  # 10 * 0.1s = 1s max wait
                    try:
                        os.kill(pid, 0)  # Check if process exists
                        time.sleep(0.1)
                    except (ProcessLookupError, PermissionError):
                        break
                return True
            except (ProcessLookupError, PermissionError):
                pass
        return False
    
    async def ensure_port_available(self) -> None:
        """Ensure the port is available, stop any process using it if necessary."""
        is_used, pid = self.is_port_in_use(self.port, self.host)
        if is_used:
            logger.warning(f"Port {self.port} is in use by process {pid}, attempting to stop it...")
            if self.stop_process_on_port(self.port, self.host):
                logger.info(f"Successfully stopped process on port {self.port}")
            else:
                raise RuntimeError(f"Could not stop process on port {self.port}. Please stop it manually and try again.")

    def _setup_routes(self):
        """Setup FastAPI routes for the service."""

        @self.app.get("/health")
        async def health_check():
            """Health check endpoint."""
            script_exists = self.script_path.exists()
            return {
                "status": "healthy" if script_exists else "unhealthy",
                "script_name": self.script_name,
                "script_exists": script_exists,
                "script_path": str(self.script_path),
            }

        @self.app.post("/run", response_model=ScriptResponse)
        async def run_script(request: ScriptRequest, background_tasks: BackgroundTasks):
            """Execute the shell script."""
            if not self.script_path.exists():
                raise HTTPException(status_code=404, detail="Script not found")

            if request.async_execution:
                task_id = f"{self.script_name}_{asyncio.get_event_loop().time()}"
                background_tasks.add_task(
                    self._run_script_async, task_id, request.parameters
                )
                return ScriptResponse(
                    status="started",
                    output=f"Script started asynchronously with task ID: {task_id}",
                    execution_time=0.0,
                )
            else:
                return await self._run_script_sync(request.parameters)

        @self.app.get("/status/{task_id}")
        async def get_task_status(task_id: str):
            """Get status of async task."""
            if task_id in self.running_processes:
                process = self.running_processes[task_id]
                if process.poll() is None:
                    return {"status": "running", "pid": process.pid}
                else:
                    return {"status": "completed", "return_code": process.returncode}
            return {"status": "not_found"}

        @self.app.get("/info")
        async def get_script_info():
            """Get information about the script."""
            return {
                "name": self.script_name,
                "path": str(self.script_path),
                "exists": self.script_path.exists(),
                "size": self.script_path.stat().st_size
                if self.script_path.exists()
                else 0,
                "executable": os.access(self.script_path, os.X_OK)
                if self.script_path.exists()
                else False,
            }

    async def _run_script_sync(self, parameters: Dict[str, Any]) -> ScriptResponse:
        """Run script synchronously."""
        import time

        start_time = time.time()

        try:
            cmd = self._build_command(parameters)

            process = await asyncio.create_subprocess_exec(
                *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            execution_time = time.time() - start_time

            return ScriptResponse(
                status="completed" if process.returncode == 0 else "failed",
                output=stdout.decode(),
                error=stderr.decode() if stderr else None,
                execution_time=execution_time,
                pid=process.pid,
            )

        except Exception as e:
            return ScriptResponse(
                status="failed",
                output="",
                error=str(e),
                execution_time=time.time() - start_time,
            )

    async def _run_script_async(self, task_id: str, parameters: Dict[str, Any]):
        """Run script asynchronously."""
        try:
            cmd = self._build_command(parameters)
            process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            self.running_processes[task_id] = process

            # Wait for completion and cleanup
            process.wait()
            if task_id in self.running_processes:
                del self.running_processes[task_id]

        except Exception as e:
            logger.error(f"Error in async execution: {e}")
            if task_id in self.running_processes:
                del self.running_processes[task_id]

    def _build_command(self, parameters: Dict[str, Any]) -> List[str]:
        """Build command with parameters."""
        # Ensure script path is absolute and executable
        script_path = self.script_path.resolve()
        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")
        
        # Make sure script is executable
        if not os.access(script_path, os.X_OK):
            try:
                script_path.chmod(0o755)  # Make script executable
            except Exception as e:
                logger.warning(f"Could not make script executable: {e}")
        
        # Build command with parameters
        cmd = [str(script_path)]
        
        # Special handling for shell script parameters
        # If there's only one parameter named 'args', pass it directly as positional arguments
        if len(parameters) == 1 and 'args' in parameters:
            # Split the args string into a list of arguments
            import shlex
            try:
                cmd.extend(shlex.split(str(parameters['args'])))
            except Exception as e:
                logger.warning(f"Error parsing args: {e}")
                cmd.append(str(parameters['args']))
        else:
            # Handle named parameters
            for key, value in parameters.items():
                if value is None:
                    continue
                if isinstance(value, bool):
                    if value:
                        cmd.append(f"--{key}")
                else:
                    # For non-boolean values, pass as positional arguments
                    cmd.append(str(value))

        logger.debug(f"Running command: {' '.join(cmd)}")
        return cmd
