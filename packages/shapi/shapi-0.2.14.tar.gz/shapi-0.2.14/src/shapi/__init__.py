"""
shapi - Shell to API Service Generator

Transform your bash scripts into production-ready APIs with REST, WebRTC, and gRPC support.
"""

__version__ = "0.2.0"
__author__ = "Tom Sapletta"
__email__ = "info@softreck.dev"

from .core import ShapiService
from .generator import ServiceGenerator
from .cli import main

__all__ = ["ShapiService", "ServiceGenerator", "main"]
