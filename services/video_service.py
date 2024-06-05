"""
This module contains the VideoService class which is responsible for reading video frames from a video file.
"""
import cv2
from utils.logger import logger


class VideoService:
    """
    Video service class to read video frames from a video file and yield them as bytes
    """
    def __init__(self, video_path):
        """
        Constructor for VideoService class
        :param video_path: Path to the video file
        """
        self.video_path = video_path

    async def video_frame_generator(self):
        """
        Generator function to read video frames from a video file and yield them as bytes
        :return: frame_bytes
        """
        video = cv2.VideoCapture(self.video_path)
        try:
            while True:
                success, frame = video.read()
                if not success:
                    break
                ret, buffer = cv2.imencode('.jpg', frame)
                if not ret:
                    raise ValueError("Failed to encode frame")
                frame_bytes = buffer.tobytes()
                yield frame_bytes
        except cv2.error as e:
            logger.exception("OpenCV error in video_frame_generator")
            raise
        except Exception as e:
            logger.exception("Error in video_frame_generator")
            raise
        finally:
            video.release()

    async def process_video(self):
        """
        Process video frames and yield them as bytes for streaming over websocket
        :return: frame_bytes
        """
        async for frame_bytes in self.video_frame_generator():
            yield frame_bytes
