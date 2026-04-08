"""WebSocket endpoint for real-time dashboard data."""

import asyncio
import json
import random
from datetime import datetime

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter()


@router.websocket("/ws/realtime")
async def realtime_ws(websocket: WebSocket):
    """Push real-time metrics every 3 seconds."""
    await websocket.accept()

    try:
        while True:
            payload = {
                "timestamp": datetime.now().isoformat(),
                "online_users": random.randint(85_000, 95_000),
                "casts_per_minute": random.randint(2_000, 2_800),
                "revenue_per_minute": round(random.uniform(280, 380), 2),
            }
            await websocket.send_json(payload)
            await asyncio.sleep(3)
    except WebSocketDisconnect:
        pass
    except Exception:
        await websocket.close()
