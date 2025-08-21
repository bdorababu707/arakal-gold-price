from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from contextlib import asynccontextmanager
from app.websocket_manager import WebSocketManager
from app.background import fetch_live_price, last_known
from app.utils.log_setup import setup_logging, get_logger
import asyncio

setup_logging()
logger = get_logger(__name__)

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    fetcher_task = asyncio.create_task(fetch_live_price())
    yield
    # Shutdown logic
    fetcher_task.cancel()
    try:
        await fetcher_task
    except asyncio.CancelledError:
        pass

app.router.lifespan_context = lifespan

@app.websocket("/ws/live-prices")
async def prices_websocket(websocket: WebSocket):
    await WebSocketManager.connect(websocket)
    try:
        while True:
            await asyncio.sleep(10)  # keep-alive
    except WebSocketDisconnect:
        await WebSocketManager.disconnect(websocket)

# ✅ Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "connected_clients": len(WebSocketManager.clients),
        "last_known": last_known,
    }
