from PIL import Image
from utils.logger import get_logger

class FramePreprocessor:
    def __init__(self, detail: str = "low"):
        self.detail = detail
        self.logger = get_logger(self.__class__.__name__)

    def preprocess(self, frames):
        size = (512, 512) if self.detail == "low" else (1024, 1024)
        processed = []
        for i, frame in enumerate(frames):
            img = frame.resize(size, Image.BICUBIC)
            processed.append(img)
        self.logger.info(f"Preprocessed {len(processed)} frames to size {size}.")
        return processed 