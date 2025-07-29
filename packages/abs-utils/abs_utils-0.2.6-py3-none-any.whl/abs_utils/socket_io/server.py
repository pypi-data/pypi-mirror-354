import socketio
from fastapi import FastAPI
from typing import Callable, Dict, Any
from functools import wraps
import asyncio
from ..logger import setup_logger

logger = setup_logger(__name__)
class SocketIOService:
    def __init__(self, cors_origins: str = "*"):
        self.sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins=cors_origins)

    def bind_app(self, fastapi_app: FastAPI):
        return socketio.ASGIApp(self.sio, other_asgi_app=fastapi_app)

    async def emit_to_sid(self, sid: str, event: str, data: Dict[str, Any]):
        await self.sio.emit(event, data, to=sid)

    async def emit_broadcast(self, event: str, data: Dict[str, Any],namespace:str=None):
        if namespace:
            await self.sio.emit(event, data,namespace=namespace)
        else:
            await self.sio.emit(event, data)

    async def join_room(self, sid: str, room: str):
        await self.sio.enter_room(sid, room)
        logger.info(f"{sid} joined room {room}")

    async def leave_room(self, sid: str, room: str):
        await self.sio.leave_room(sid, room)
        logger.info(f"{sid} left room {room}")

    async def emit_to_room(self, event: str, room: str, data: Dict[str, Any], namespace: str = None):
        await self.sio.emit(event, data, room=room, namespace=namespace)
