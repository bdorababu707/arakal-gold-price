from fastapi import WebSocket
from typing import List
from app.utils.log_setup import get_logger

logger = get_logger(__name__)

class WebSocketManager:
    clients: List[WebSocket] = []

    @staticmethod
    async def connect(websocket: WebSocket):
        await websocket.accept()
        WebSocketManager.clients.append(websocket)
        logger.info("Client connected. Total clients: %d", len(WebSocketManager.clients))

    @staticmethod
    async def disconnect(websocket: WebSocket):
        if websocket in WebSocketManager.clients:
            WebSocketManager.clients.remove(websocket)
            logger.info("Client disconnected. Total clients: %d", len(WebSocketManager.clients))

    @staticmethod
    async def broadcast(message: dict):
        disconnected = []
        for client in WebSocketManager.clients:
            try:
                await client.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send to client: {e}")
                disconnected.append(client)

        for client in disconnected:
            await WebSocketManager.disconnect(client)
