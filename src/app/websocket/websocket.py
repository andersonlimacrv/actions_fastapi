from typing import Annotated
from fastapi import WebSocket, HTTPException, status, WebSocketDisconnect, APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.app.models.user import User
from src.app.core.security import get_current_user_ws
from src.app.core.database.db import async_get_db_session
from src.app.websocket.ws_manager import WebSocketManager
import json


ws_manager = WebSocketManager()
ws_router = APIRouter(tags=["WebSocket 🔥"])

CurrentUser = Annotated[User, Depends(get_current_user_ws)]
db_session = Annotated[AsyncSession, Depends(async_get_db_session)]

@ws_router.websocket("/ws/{endpoint}")
async def websocket_endpoint(websocket: WebSocket, endpoint: str, db: db_session):
    try:
        await ws_manager.connect(websocket, endpoint)

        token = await ws_manager.get_token_from_first_message(websocket)
        
        await get_current_user_ws(token, db)
        
        while True:
            data = await websocket.receive_text()
            await ws_manager.broadcast(endpoint, f"Message from {endpoint}: {data}")
    
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket, endpoint)
    except HTTPException as e:
        print(f"HTTP Error { e.status_code} - {e.detail}")
        await websocket.close()
    except Exception as e:
        print(f"Error: {e}")
        await websocket.close()