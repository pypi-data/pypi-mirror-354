"""
WebRTC protocol implementation for real-time communication.
"""

import asyncio
import json
import logging
from typing import Dict, Any, Set
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel
from aiortc.contrib.signaling import BYE, add_signaling_arguments, create_signaling
import websockets

logger = logging.getLogger(__name__)


class WebRTCProtocol:
    """WebRTC protocol for real-time script execution and data streaming."""

    def __init__(self, host: str = "localhost", port: int = 8765):
        self.host = host
        self.port = port
        self.connections: Set[RTCPeerConnection] = set()

    async def handle_websocket(self, websocket, path):
        """Handle WebSocket connections for WebRTC signaling."""
        pc = RTCPeerConnection()
        self.connections.add(pc)

        @pc.on("datachannel")
        def on_datachannel(channel: RTCDataChannel):
            logger.info(f"Data channel established: {channel.label}")

            @channel.on("message")
            def on_message(message):
                if isinstance(message, str):
                    try:
                        data = json.loads(message)
                        # Handle script execution request
                        asyncio.create_task(self.handle_script_request(channel, data))
                    except json.JSONDecodeError:
                        channel.send(json.dumps({"error": "Invalid JSON"}))

        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    await self.handle_signaling(pc, websocket, data)
                except json.JSONDecodeError:
                    await websocket.send(json.dumps({"error": "Invalid JSON"}))
        except websockets.exceptions.ConnectionClosed:
            pass
        finally:
            await pc.close()
            self.connections.discard(pc)

    async def handle_signaling(
        self, pc: RTCPeerConnection, websocket, data: Dict[str, Any]
    ):
        """Handle WebRTC signaling messages."""
        if data.get("type") == "offer":
            await pc.setRemoteDescription(
                RTCSessionDescription(sdp=data["sdp"], type=data["type"])
            )

            answer = await pc.createAnswer()
            await pc.setLocalDescription(answer)

            await websocket.send(
                json.dumps({"type": "answer", "sdp": pc.localDescription.sdp})
            )

        elif data.get("type") == "ice-candidate":
            await pc.addIceCandidate(data["candidate"])

    async def handle_script_request(
        self, channel: RTCDataChannel, data: Dict[str, Any]
    ):
        """Handle script execution request via WebRTC."""
        try:
            script_name = data.get("script")
            parameters = data.get("parameters", {})

            # Simulate script execution
            result = {
                "status": "success",
                "output": f"Executed {script_name} with {parameters}",
                "timestamp": asyncio.get_event_loop().time(),
            }

            channel.send(json.dumps(result))

        except Exception as e:
            error_response = {"status": "error", "message": str(e)}
            channel.send(json.dumps(error_response))

    async def start_server(self):
        """Start WebRTC signaling server."""
        logger.info(f"Starting WebRTC signaling server on {self.host}:{self.port}")

        async with websockets.serve(
            self.handle_websocket, self.host, self.port
        ) as server:
            logger.info("WebRTC server started")
            await server.wait_closed()
