"""
Service generator for creating API wrappers for shell scripts.
"""

import os
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader
import yaml

from .templates import get_template_content


class ServiceGenerator:
    """Generate API service files for shell scripts."""

    def __init__(self, output_dir: str = "./generated"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate_service(
        self,
        script_path: str,
        script_name: str,
        service_config: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate complete service structure for a shell script."""

        service_dir = self.output_dir / script_name
        service_dir.mkdir(exist_ok=True)

        config = service_config or {}

        # Generate main service file
        self._generate_main_py(service_dir, script_path, script_name, config)

        # Generate Dockerfile
        self._generate_dockerfile(service_dir, script_name, config)

        # Generate Makefile
        self._generate_makefile(service_dir, script_name, config)

        # Generate test file
        self._generate_test_py(service_dir, script_name, config)

        # Generate Ansible playbook
        self._generate_ansible_test(service_dir, script_name, config)

        # Generate requirements.txt
        self._generate_requirements(service_dir, config)

        # Generate docker-compose.yml
        self._generate_docker_compose(service_dir, script_name, config)

        # Copy original script
        script_source = Path(script_path)
        if script_source.exists():
            shutil.copy2(script_source, service_dir / script_source.name)

        return str(service_dir)

    def _generate_main_py(
        self, service_dir: Path, script_path: str, script_name: str, config: Dict
    ):
        """Generate main.py file."""
        content = get_template_content("main.py.j2").render(
            script_path=script_path, script_name=script_name, config=config
        )
        (service_dir / "main.py").write_text(content)

    def _generate_dockerfile(self, service_dir: Path, script_name: str, config: Dict):
        """Generate Dockerfile."""
        content = get_template_content("Dockerfile.j2").render(
            script_name=script_name, config=config
        )
        (service_dir / "Dockerfile").write_text(content)

    def _generate_makefile(self, service_dir: Path, script_name: str, config: Dict):
        """Generate Makefile."""
        content = get_template_content("Makefile.j2").render(
            script_name=script_name, config=config
        )
        (service_dir / "Makefile").write_text(content)

    def _generate_test_py(self, service_dir: Path, script_name: str, config: Dict):
        """Generate test.py file."""
        content = get_template_content("test.py.j2").render(
            script_name=script_name, config=config
        )
        (service_dir / "test_service.py").write_text(content)

    def _generate_ansible_test(self, service_dir: Path, script_name: str, config: Dict):
        """Generate Ansible test playbook."""
        ansible_dir = service_dir / "ansible"
        ansible_dir.mkdir(exist_ok=True)

        content = get_template_content("ansible_test.yml.j2").render(
            script_name=script_name, config=config
        )
        (ansible_dir / "test.yml").write_text(content)

    def _generate_requirements(self, service_dir: Path, config: Dict):
        """Generate requirements.txt."""
        content = get_template_content("requirements.txt.j2").render(config=config)
        (service_dir / "requirements.txt").write_text(content)

    def _generate_docker_compose(
        self, service_dir: Path, script_name: str, config: Dict
    ):
        """Generate docker-compose.yml."""
        content = get_template_content("docker-compose.yml.j2").render(
            script_name=script_name, config=config
        )
        (service_dir / "docker-compose.yml").write_text(content)
