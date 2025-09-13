from fastapi import WebSocket
from typing import List
from app.utils.log_setup import get_logger
import asyncio

logger = get_logger(__name__)

class WebSocketManager:
    clients: List[WebSocket] = []

    @staticmethod
    async def connect(websocket: WebSocket):
        await websocket.accept()
        WebSocketManager.clients.append(websocket)

    @staticmethod
    async def disconnect(websocket: WebSocket):
        if websocket in WebSocketManager.clients:
            WebSocketManager.clients.remove(websocket)

    @staticmethod
    async def broadcast(message: dict):
        if not WebSocketManager.clients:
            return  # No clients, skip

        # Create send tasks for all clients
        tasks = [client.send_json(message) for client in WebSocketManager.clients]

        # Run all sends concurrently, don't raise exceptions
        results = await asyncio.gather(*tasks, return_exceptions=True)

        # Collect clients that failed
        disconnected = []
        for client, result in zip(WebSocketManager.clients, results):
            if isinstance(result, Exception):
                disconnected.append(client)

        # Remove failed clients
        for client in disconnected:
            await WebSocketManager.disconnect(client)
