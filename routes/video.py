"""
This module contains the FastAPI router for video streaming.
"""

from fastapi import APIRouter, WebSocket, HTTPException
from services.video_service import VideoService
from utils.logger import logger

video_router = APIRouter()


@video_router.websocket("/ws_video")
async def websocket_endpoint(websocket: WebSocket):
    """
    Websocket endpoint for video streaming service
    :param websocket: WebSocket
    :return: None
    """
    await websocket.accept()
    video_path = 'sample.mp4'
    video_service = VideoService(video_path)
    try:
        async for frame in video_service.process_video():
            await websocket.send_bytes(frame)
    except HTTPException as e:
        logger.exception("HTTP error in websocket_endpoint")
        await websocket.close(code=e.status_code, reason=e.detail)
        raise
    except Exception as e:
        logger.exception("Error in websocket_endpoint")
        await websocket.close(code=1011, reason="Internal Server Error")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    finally:
        await websocket.close()
