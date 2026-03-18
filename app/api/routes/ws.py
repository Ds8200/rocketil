from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.services.broadcaster import manager

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(ws: WebSocket) -> None:
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  # keep connection alive, ignore incoming messages
    except WebSocketDisconnect:
        manager.disconnect(ws)
