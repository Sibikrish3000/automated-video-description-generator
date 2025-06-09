import os
import cv2
from utils.logger import get_logger

class VideoIngestor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.logger = get_logger(self.__class__.__name__)

    def load(self):
        if not os.path.exists(self.video_path):
            self.logger.error("Video file not found: %s", self.video_path)
            raise FileNotFoundError("Video file not found: %s", self.video_path)
        cap = cv2.VideoCapture(self.video_path)  # type: ignore[attr-defined]
        if not cap.isOpened():
            self.logger.error("Cannot open video file: %s", self.video_path)
            raise IOError("Cannot open video file: %s", self.video_path)
        self.logger.info("Video file loaded: %s", self.video_path)
        cap.release()
        return self.video_path
        