"""
App code, references FastAPI to create a FastAPI app.
"""

import threading
from fastapi import FastAPI
from fastapi.responses import FileResponse
from routes.video import video_router


class SingletonFastAPI(FastAPI):
    """
    Singleton pattern for FastAPI app
    """
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        """
        Singleton pattern for FastAPI app
        :return: FastAPI app instance
        """
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
        return cls._instance


app = SingletonFastAPI()
app.include_router(video_router)


@app.get("/")
async def read_root():
    """
    Root endpoint
    :return: Welcome message
    """
    return {"message": "Welcome to the WebSocket Video Streaming Service"}


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    """
    Favicon endpoint
    :return: Favicon
    """
    return FileResponse("path/to/favicon.ico")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
