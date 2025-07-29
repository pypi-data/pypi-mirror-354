"""
Service manager for tracking and managing running shapi services.
"""
import json
import os
import signal
import sys
import time
from dataclasses import dataclass, asdict, field, fields
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any

import psutil

SERVICE_FILE = os.environ.get("SHAPI_SERVICE_FILE") or str(Path.home() / ".shapi" / "services.json")

@dataclass
class ServiceInfo:
    """Information about a running shapi service."""
    name: str
    pid: int
    port: int
    host: str
    script_path: str
    start_time: float = field(default_factory=time.time)
    log_file: Optional[str] = None
    
    def __post_init__(self):
        """Handle any post-initialization processing."""
        # Convert string paths to Path objects if needed
        if isinstance(self.script_path, str):
            self.script_path = Path(self.script_path)

    @property
    def uptime(self) -> str:
        """Get formatted uptime of the service."""
        uptime_seconds = int(time.time() - self.start_time)
        hours, remainder = divmod(uptime_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

    @property
    def status(self) -> str:
        """Get the status of the service (running/stopped)."""
        try:
            process = psutil.Process(self.pid)
            if process.status() == psutil.STATUS_ZOMBIE:
                return "zombie"
            return "running"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return "stopped"

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        data = {}
        for f in fields(self):
            value = getattr(self, f.name)
            # Convert Path objects to strings for JSON serialization
            if isinstance(value, Path):
                value = str(value)
            data[f.name] = value
        # Add computed fields
        data["status"] = self.status
        data["uptime"] = self.uptime
        return data

class ServiceManager:
    """Manages running shapi services."""
    
    def __init__(self, service_file: str = None):
        """Initialize the service manager."""
        self.service_file = str(Path(service_file) if service_file else SERVICE_FILE)
        self.services: Dict[int, ServiceInfo] = {}
        self._load_services()
    
    def _ensure_service_dir(self) -> None:
        """Ensure the service directory exists."""
        try:
            service_dir = os.path.dirname(self.service_file)
            if service_dir:  # Only create if there's a directory component
                os.makedirs(service_dir, exist_ok=True, mode=0o755)
        except Exception as e:
            print(f"Error creating service directory: {e}", file=sys.stderr)
            raise
    
    def _load_services(self) -> None:
        """Load services from the service file."""
        try:
            service_path = Path(self.service_file)
            if not service_path.exists():
                return
                
            with open(service_path, 'r') as f:
                data = json.load(f)
                for pid, service_data in data.items():
                    try:
                        # Remove computed fields before creating the ServiceInfo
                        service_data.pop('status', None)
                        service_data.pop('uptime', None)
                        service = ServiceInfo(**service_data)
                        if service.status == "running":
                            self.services[int(pid)] = service
                        else:
                            print(f"Service {pid} is not running (status: {service.status})", file=sys.stderr)
                    except Exception as e:
                        print(f"Error loading service {pid}: {e}", file=sys.stderr)
            self._cleanup_stopped()
        except json.JSONDecodeError as e:
            print(f"Warning: Invalid JSON in service file {self.service_file}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"Error loading services: {e}", file=sys.stderr)
    
    def _save_services(self) -> None:
        """Save services to the service file."""
        try:
            self._ensure_service_dir()
            service_path = Path(self.service_file)
            temp_path = f"{service_path}.tmp"
            
            services_dict = {}
            for pid, service in self.services.items():
                if service.status == "running":
                    services_dict[str(pid)] = service.to_dict()
            
            # Write to a temporary file first, then atomically rename
            with open(temp_path, 'w') as f:
                json.dump(services_dict, f, indent=2)
            
            # On POSIX systems, this is an atomic operation
            os.replace(temp_path, service_path)
            
        except Exception as e:
            print(f"Error saving services: {e}", file=sys.stderr)
            if 'temp_path' in locals() and os.path.exists(temp_path):
                os.unlink(temp_path)
    
    def _cleanup_stopped(self) -> None:
        """Remove stopped services from the registry."""
        stopped_pids = [pid for pid, service in self.services.items() 
                       if service.status == "stopped"]
        for pid in stopped_pids:
            del self.services[pid]
        if stopped_pids:
            self._save_services()
    
    def register_service(self, service: ServiceInfo) -> bool:
        """Register a new service.
        
        Returns:
            bool: True if registration was successful, False otherwise
        """
        try:
            self.services[service.pid] = service
            self._save_services()
            print(f"Registered service: {service.name} (PID: {service.pid})", file=sys.stderr)
            return True
        except Exception as e:
            print(f"Error registering service: {e}", file=sys.stderr)
            return False
    
    def unregister_service(self, pid: int) -> bool:
        """Unregister a service by PID."""
        if pid in self.services:
            del self.services[pid]
            self._save_services()
            return True
        return False
    
    def get_service(self, identifier: str) -> Tuple[Optional[ServiceInfo], str]:
        """Get a service by name or PID."""
        # Try to match by name
        for service in self.services.values():
            if service.name == identifier:
                return service, "name"
        
        # Try to match by PID
        try:
            pid = int(identifier)
            if pid in self.services:
                return self.services[pid], "pid"
        except ValueError:
            pass
            
        return None, ""
    
    def list_services(self) -> List[Dict]:
        """List all running services."""
        self._cleanup_stopped()
        return [
            {
                "name": service.name,
                "pid": pid,
                "port": service.port,
                "host": service.host,
                "status": service.status,
                "uptime": service.uptime,
                "script": str(service.script_path)
            }
            for pid, service in self.services.items()
        ]
    
    def stop_service(self, identifier: str, force: bool = False) -> bool:
        """Stop a running service."""
        service, _ = self.get_service(identifier)
        if not service:
            return False
            
        try:
            os.kill(service.pid, signal.SIGTERM)
            if force:
                time.sleep(1)
                if self.is_running(service.pid):
                    os.kill(service.pid, signal.SIGKILL)
            self.unregister_service(service.pid)
            return True
        except ProcessLookupError:
            self.unregister_service(service.pid)
            return False
        except Exception as e:
            print(f"Error stopping service: {e}")
            return False
    
    @staticmethod
    def is_running(pid: int) -> bool:
        """Check if a process is running."""
        try:
            process = psutil.Process(pid)
            return process.status() != psutil.STATUS_ZOMBIE
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return False
