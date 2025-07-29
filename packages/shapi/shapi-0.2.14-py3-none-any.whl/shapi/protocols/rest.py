"""
REST API protocol implementation.
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any, Optional
import asyncio
import json


class RestProtocol:
    """REST API protocol for shell script execution."""

    def __init__(self, app: FastAPI):
        self.app = app
        self.setup_routes()

    def setup_routes(self):
        """Setup REST API routes."""

        @self.app.middleware("http")
        async def add_cors_headers(request: Request, call_next):
            response = await call_next(request)
            response.headers["Access-Control-Allow-Origin"] = "*"
            response.headers[
                "Access-Control-Allow-Methods"
            ] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
            return response

        @self.app.get("/api/v1/scripts")
        async def list_scripts():
            """List available scripts."""
            return {"scripts": ["example_script"]}

        @self.app.post("/api/v1/scripts/{script_name}/execute")
        async def execute_script(script_name: str, request: Request):
            """Execute script via REST API."""
            body = await request.json()

            # Implementation would go here
            return {"status": "success", "script": script_name, "parameters": body}
