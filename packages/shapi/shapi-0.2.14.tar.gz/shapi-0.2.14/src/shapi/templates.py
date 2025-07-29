"""
Template management for shapi.
"""

from jinja2 import Environment, BaseLoader
from typing import Dict


class StringTemplateLoader(BaseLoader):
    """Template loader for string templates."""

    def __init__(self, templates: Dict[str, str]):
        self.templates = templates

    def get_source(self, environment, template):
        if template in self.templates:
            source = self.templates[template]
            return source, None, lambda: True
        raise jinja2.TemplateNotFound(template)


# Template definitions
TEMPLATES = {
    "main.py.j2": '''#!/usr/bin/env python3
"""
Generated shapi service for {{ script_name }}
"""

import uvicorn
from shapi.core import ShapiService

def main():
    service = ShapiService("{{ script_path }}", "{{ script_name }}")

    uvicorn.run(
        service.app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

if __name__ == "__main__":
    main()
''',
    "Dockerfile.j2": """FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    bash \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Make script executable
RUN chmod +x *.sh 2>/dev/null || true

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run the service
CMD ["python", "main.py"]
""",
    "Makefile.j2": """# Makefile for {{ script_name }} service

.PHONY: help install test run build clean docker-build docker-run

SERVICE_NAME := {{ script_name }}
IMAGE_NAME := shapi-$(SERVICE_NAME)
PORT := 8000

help: ## Show this help message
	@echo "Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \\033[36m%-15s\\033[0m %s\\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	python -m pytest test_service.py -v

run: ## Run the service locally
	python main.py

build: install test ## Build and test the service

docker-build: ## Build Docker image
	docker build -t $(IMAGE_NAME):latest .

docker-run: ## Run Docker container
	docker run -p $(PORT):8000 $(IMAGE_NAME):latest

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	docker rmi $(IMAGE_NAME):latest 2>/dev/null || true

deploy: docker-build ## Deploy with docker-compose
	docker-compose up -d

logs: ## Show service logs
	docker-compose logs -f

stop: ## Stop the service
	docker-compose down
""",
    "test.py.j2": '''#!/usr/bin/env python3
"""
Tests for {{ script_name }} service
"""

import pytest
import requests
import time
from fastapi.testclient import TestClient
from shapi.core import ShapiService

# Test configuration
SERVICE_NAME = "{{ script_name }}"
SCRIPT_PATH = "./{{ script_name }}.sh"


@pytest.fixture
def client():
    """Create test client."""
    service = ShapiService(SCRIPT_PATH, SERVICE_NAME)
    return TestClient(service.app)


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert "status" in data
    assert data["script_name"] == SERVICE_NAME


def test_info_endpoint(client):
    """Test script info endpoint."""
    response = client.get("/info")
    assert response.status_code == 200

    data = response.json()
    assert "name" in data
    assert data["name"] == SERVICE_NAME


def test_run_endpoint_sync(client):
    """Test synchronous script execution."""
    response = client.post("/run", json={
        "parameters": {},
        "async_execution": False
    })

    # Should return response even if script doesn't exist
    assert response.status_code in [200, 404]


def test_run_endpoint_async(client):
    """Test asynchronous script execution."""
    response = client.post("/run", json={
        "parameters": {},
        "async_execution": True
    })

    # Should return response even if script doesn't exist
    assert response.status_code in [200, 404]


def test_openapi_docs(client):
    """Test OpenAPI documentation endpoint."""
    response = client.get("/docs")
    assert response.status_code == 200


def test_openapi_json(client):
    """Test OpenAPI JSON endpoint."""
    response = client.get("/openapi.json")
    assert response.status_code == 200

    data = response.json()
    assert "info" in data
    assert "paths" in data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
''',
    "requirements.txt.j2": """fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
aiofiles>=23.0.0
python-multipart>=0.0.6
psutil>=5.9.0
pytest>=7.4.0
httpx>=0.24.0
""",
    "docker-compose.yml.j2": """version: '3.8'

services:
  {{ script_name }}:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf:ro
    depends_on:
      - {{ script_name }}
    restart: unless-stopped
""",
    "ansible_test.yml.j2": """---
- name: Test {{ script_name }} service deployment
  hosts: localhost
  connection: local
  vars:
    service_name: {{ script_name }}
    service_port: 8000

  tasks:
    - name: Check if Docker is installed
      command: docker --version
      register: docker_version
      failed_when: false

    - name: Install Docker if not present
      package:
        name: docker.io
        state: present
      when: docker_version.rc != 0
      become: yes

    - name: Start Docker service
      service:
        name: docker
        state: started
        enabled: yes
      become: yes

    - name: Build Docker image
      docker_image:
        name: "shapi-{{ service_name }}"
        build:
          path: "."
        source: build

    - name: Run container
      docker_container:
        name: "{{ service_name }}-test"
        image: "shapi-{{ service_name }}"
        ports:
          - "{{ service_port }}:8000"
        state: started
        restart_policy: always

    - name: Wait for service to be ready
      uri:
        url: "http://localhost:{{ service_port }}/health"
        method: GET
      register: health_check
      until: health_check.status == 200
      retries: 30
      delay: 2

    - name: Test service endpoints
      uri:
        url: "http://localhost:{{ service_port }}/{{ item }}"
        method: GET
      loop:
        - health
        - info
        - docs
        - openapi.json

    - name: Run service tests
      command: python -m pytest test_service.py -v

    - name: Cleanup test container
      docker_container:
        name: "{{ service_name }}-test"
        state: absent
      when: cleanup | default(true)
""",
}


def get_template_content(template_name: str):
    """Get template content by name."""
    env = Environment(loader=StringTemplateLoader(TEMPLATES))
    return env.get_template(template_name)
