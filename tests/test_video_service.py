"""
This module contains tests for the video_service module.
"""
import pytest
from services.video_service import VideoService


@pytest.fixture
def video_service():
    """
    Create a VideoService instance for testing
    :return: VideoService instance
    """
    return VideoService('sample.mp4')


@pytest.mark.asyncio
async def test_video_frame_generator(video_service):
    """
    Test the video_frame_generator method
    :param video_service: VideoService instance
    :return: None
    """
    frame_generator = video_service.video_frame_generator()
    frame_count = 0
    async for frame in frame_generator:
        assert isinstance(frame, bytes)
        frame_count += 1

    # Ensure that we processed some frames
    assert frame_count > 0


@pytest.mark.asyncio
async def test_process_video(video_service):
    """
    Test the process_video method
    :param video_service: VideoService instance
    :return: None
    """
    video_processor = video_service.process_video()
    frame_count = 0
    async for frame in video_processor:
        assert isinstance(frame, bytes)
        frame_count += 1

    # Ensure that we processed some frames
    assert frame_count > 0
