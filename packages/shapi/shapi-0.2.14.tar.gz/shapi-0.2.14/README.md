<div align="center">
  <h1>✨ shapi</h1>
  <p>Transform shell scripts into production-ready APIs with REST, WebRTC, and gRPC support</p>
  
  [![PyPI Version](https://img.shields.io/pypi/v/shapi?color=blue)](https://pypi.org/project/shapi/)
  [![Python Versions](https://img.shields.io/pypi/pyversions/shapi)](https://pypi.org/project/shapi/)
  [![License](https://img.shields.io/github/license/wronai/shapi)](https://github.com/wronai/shapi/blob/main/LICENSE)
  [![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
  [![Documentation](https://img.shields.io/badge/docs-latest-blue.svg)](https://wronai.github.io/shapi/)
  [![Tests](https://github.com/wronai/shapi/actions/workflows/tests.yml/badge.svg)](https://github.com/wronai/shapi/actions)
  [![Codecov](https://codecov.io/gh/wronai/shapi/branch/main/graph/badge.svg)](https://codecov.io/gh/wronai/shapi)

  [🚀 Quick Start](#-quick-start) |
  [📖 Documentation](https://wronai.github.io/shapi/) |
  [💡 Examples](#-examples) |
  [🤝 Contributing](#-contributing) |
  [📄 License](#-license)
</div>

## ✨ Features

- 🚀 **Instant API Generation**: Convert any shell script into a REST API with a single command
- 🤖 **AI-Powered**: Leverage local LLM (Mistral:7b) for intelligent API generation
- 🐳 **Container Ready**: Automatic Dockerfile and docker-compose.yml generation
- 🌐 **Multi-Protocol**: Support for REST, WebRTC, and gRPC APIs
- 🧪 **Testing Included**: Generated test suites and Ansible playbooks
- 📊 **Monitoring**: Built-in health checks and status endpoints
- 🔧 **Service Management**: Start, stop, and manage multiple services
- 🚦 **Port Management**: Automatic port conflict resolution
- 🎯 **Daemon Mode**: Run services in the background
- 🔄 **Service Discovery**: List and manage running services

## 📦 Installation

```bash
# Install using pip
pip install shapi

# Or install from source
git clone https://github.com/wronai/shapi.git
cd shapi
pip install -e .
```

## 🚀 Quick Start

### Serve a Script

```bash
# Serve a script directly
shapi serve ./examples/echo.sh --port 8000

# Or run it as a daemon
shapi serve ./examples/echo.sh --name echo-service --port 8000 --daemon

# List running services
shapi service list
```

### Manage Services

```bash
# List all running services
shapi service list

# Stop a service
shapi service stop service-name

# Restart a service
shapi service restart service-name

# Force stop if port is in use
shapi serve ./script.sh --port 8000 --force
```

### Generate Service Structure

```bash
# Generate complete service structure with Docker and tests
shapi generate /path/to/your/script.sh --name my-service

# Navigate to the generated service
cd my-service

# Install dependencies and run
pip install -r requirements.txt
python main.py
```

## 📚 Documentation

- [Examples](./examples/README.md) - Detailed documentation of example scripts
- [API Reference](https://wronai.github.io/shapi/) - Complete API documentation
- [Development Guide](./CONTRIBUTING.md) - How to contribute to ShAPI

## 🔍 Examples

ShAPI comes with several example scripts that demonstrate its capabilities:

1. `ls.sh` - List directory contents
2. `ps.sh` - Show running processes
3. `df.sh` - Display disk usage
4. `free.sh` - Show memory usage
5. `whoami.sh` - Display current user information
6. `date.sh` - Show current date/time with formatting
7. `echo.sh` - Echo back input text

See the [examples documentation](./examples/README.md) for detailed usage and API examples.

## 🛠️ Project Structure

```
my-service/
├── main.py              # FastAPI service
├── Dockerfile           # Container configuration
├── docker-compose.yml   # Multi-service setup
├── Makefile            # Build and deployment commands
├── requirements.txt    # Python dependencies
├── test_service.py     # Test suite
├── ansible/           # Infrastructure tests
│   └── test.yml
└── script.sh          # Your original script
```

## Usage Examples

### Basic Script Conversion

```bash
#!/bin/bash
# hello.sh
echo "Hello, $1!"
```

Generate the service:
```bash
shapi generate hello.sh --name greeting-service
cd greeting-service
python main.py
```

Access your API:
- **Health Check**: `GET http://localhost:8000/health`
- **Documentation**: `GET http://localhost:8000/docs`
- **Execute Script**: `POST http://localhost:8000/run`

### API Endpoints

Every generated service includes:

- `GET /health` - Service health check
- `GET /info` - Script information
- `POST /run` - Execute script (sync/async)
- `GET /status/{task_id}` - Check async task status
- `GET /docs` - Interactive API documentation

## Service Management

### Managing Multiple Services

```bash
# Start multiple services on different ports
shapi serve ./service1.sh --name service1 --port 8000 --daemon
shapi serve ./service2.sh --name service2 --port 8001 --daemon

# List all running services
shapi service list

# Output:
# ┏━━━━━━━━━━━┳━━━━━━━━┳━━━━━━┳━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
# ┃ Name      ┃ PID    ┃ Port ┃ Status  ┃ Uptime   ┃ Script                          ┃
# ┡━━━━━━━━━━━╇━━━━━━━━╇━━━━━━╇━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
# │ service1  │ 12345  │ 8000 │ running │ 00:05:32 │ /path/to/service1.sh            │
# │ service2  │ 12346  │ 8001 │ running │ 00:02:15 │ /path/to/service2.sh            │
# └───────────┴────────┴──────┴─────────┴──────────┴─────────────────────────────────┘

# Stop a service
shapi service stop service1

# Force stop a service if it's not responding
shapi service stop service2 --force

# Restart a service
shapi service restart service1
```

### Port Management

```bash
# Start a service with automatic port conflict resolution
shapi serve ./service.sh --port 8000 --force

# The --force flag will automatically stop any service using port 8000
```

### Example API Request

```json
POST /run
{
  "parameters": {
    "name": "World",
    "verbose": true
  },
  "async_execution": false
}
```

### Docker Deployment

```bash
# Build and run with Docker
make docker-build
make docker-run

# Or use docker-compose
docker-compose up -d
```

### Testing

```bash
# Run tests
make test

# Or directly
python -m pytest test_service.py -v
```

## Configuration

Create a `config.yaml` file for advanced configuration:

```yaml
service:
  name: "my-advanced-service"
  description: "Advanced shell script API"
  version: "1.0.0"
  
protocols:
  rest: true
  grpc: true
  webrtc: true
  
security:
  auth_required: false
  cors_enabled: true
  
monitoring:
  health_check_interval: 30
  metrics_enabled: true
```

## CLI Commands

```bash
# Generate service structure
shapi generate hello.sh --name service-name --output ./output

# Serve script directly
shapi serve hello.sh --host 0.0.0.0 --port 8008

# Test generated service
shapi test ./generated/service-name

# Build Docker image
shapi build ./generated/service-name
```

## Advanced Features

### Async Execution

```python
# Enable async execution for long-running scripts
response = requests.post("/run", json={
    "parameters": {"input": "data"},
    "async_execution": True
})

task_id = response.json()["task_id"]

# Check status
status = requests.get(f"/status/{task_id}")
```

### Multiple Protocols

The generated service supports multiple communication protocols:

- **REST API**: Standard HTTP endpoints
- **WebRTC**: Real-time data streaming
- **gRPC**: High-performance RPC calls

### Production Deployment

```bash
# Using Makefile
make deploy

# Manual deployment
docker-compose up -d
```

## Requirements

- Python 3.8+
- Docker (optional, for containerization)
- Bash (for shell script execution)

## Contributing

Contributions are welcome! Please see our [Contributing Guidelines](CONTRIBUTING.md).

## License

Apache License 2.0 - see [LICENSE](LICENSE) file for details.

## Support

- 📖 [Documentation](https://wronai.github.io/shapi)
- 🐛 [Issue Tracker](https://github.com/wronai/shapi/issues)
- 💬 [Discussions](https://github.com/wronai/shapi/discussions)

---

**shapi** - From shell to service in seconds! 🚀







# Contributing Guidelines
# CONTRIBUTING.md
"""
# Contributing to shapi

We welcome contributions to shapi! This document provides guidelines for contributing.

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/wronai/shapi.git
cd shapi
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install in development mode:
```bash
pip install -e .[dev]
```

## Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=shapi

# Run specific test file
pytest tests/test_core.py -v
```

## Code Style

We use black for code formatting and flake8 for linting:

```bash
# Format code
black shapi/

# Check linting
flake8 shapi/
```

## Submitting Changes

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Reporting Issues

Please use the GitHub issue tracker to report bugs or request features.
"""