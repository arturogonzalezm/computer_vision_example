"""
This module contains tests for the WebSocket endpoint.
"""

import pytest
from fastapi.testclient import TestClient
from starlette.websockets import WebSocketDisconnect

from app import app


@pytest.fixture
def client():
    """
    Create a test client for the FastAPI app.
    :return: TestClient
    """
    return TestClient(app)


@pytest.mark.asyncio
async def test_websocket_endpoint(client):
    """
    Test the WebSocket endpoint.
    :param client: TestClient
    :return: None
    """
    with client.websocket_connect("/ws_video") as websocket:
        frame_count = 0
        try:
            for _ in range(10):  # Limit the number of frames for the test
                data = websocket.receive_bytes()
                assert isinstance(data, bytes)
                frame_count += 1
        except WebSocketDisconnect:
            pass

        # Ensure that we received some frames
        assert frame_count > 0
