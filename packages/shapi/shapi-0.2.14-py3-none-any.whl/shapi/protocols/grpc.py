"""
gRPC protocol implementation.
"""

import grpc
import asyncio
from concurrent import futures
from typing import Dict, Any
import grpc.aio
from grpc_reflection.v1alpha import reflection
from grpc_health.v1alpha import health
from grpc_health.v1alpha import health_pb2
from grpc_health.v1alpha import health_pb2_grpc


class GrpcProtocol:
    """gRPC protocol for shell script execution."""

    def __init__(self, port: int = 50051):
        self.port = port
        self.server = None

    async def start_server(self):
        """Start gRPC server."""
        self.server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10))

        # Add health check service
        health_servicer = health.HealthServicer()
        health_pb2_grpc.add_HealthServicer_to_server(health_servicer, self.server)

        # Add reflection service
        SERVICE_NAMES = (
            health_pb2.DESCRIPTOR.services_by_name["Health"].full_name,
            reflection.SERVICE_NAME,
        )
        reflection.enable_server_reflection(SERVICE_NAMES, self.server)

        listen_addr = f"[::]:{self.port}"
        self.server.add_insecure_port(listen_addr)

        await self.server.start()
        print(f"gRPC server started on {listen_addr}")

        try:
            await self.server.wait_for_termination()
        except KeyboardInterrupt:
            await self.server.stop(0)
