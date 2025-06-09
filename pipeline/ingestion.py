import os
import cv2
from utils.logger import get_logger

class VideoIngestor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.logger = get_logger(self.__class__.__name__)

    def load(self):
        if not os.path.exists(self.video_path):
            self.logger.error(f"Video file not found: {self.video_path}")
            raise FileNotFoundError(f"Video file not found: {self.video_path}")
        cap = cv2.VideoCapture(self.video_path)  # type: ignore[attr-defined]
        if not cap.isOpened():
            self.logger.error(f"Cannot open video file: {self.video_path}")
            raise IOError(f"Cannot open video file: {self.video_path}")
        self.logger.info(f"Video file loaded: {self.video_path}")
        cap.release()
        return self.video_path 