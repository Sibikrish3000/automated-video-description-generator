import cv2
from PIL import Image
import numpy as np
from utils.logger import get_logger

class FrameExtractor:
    def __init__(self, num_frames: int = 10):
        self.num_frames = num_frames
        self.logger = get_logger(self.__class__.__name__)

    def extract(self, video_path: str):
        cap = cv2.VideoCapture(video_path)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        if total_frames < self.num_frames:
            self.logger.warning(f"Video has fewer frames ({total_frames}) than requested ({self.num_frames}).")
            frame_indices = list(range(total_frames))
        else:
            frame_indices = np.linspace(0, total_frames - 1, self.num_frames, dtype=int)
        frames = []
        for idx in frame_indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if not ret:
                self.logger.warning(f"Failed to read frame at index {idx}.")
                continue
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_img = Image.fromarray(frame_rgb)
            frames.append(pil_img)
        cap.release()
        self.logger.info(f"Extracted {len(frames)} frames from {video_path}.")
        return frames 