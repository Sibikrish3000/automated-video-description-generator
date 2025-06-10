import os
import sys
import glob
import yaml
from pipeline.ingestion import VideoIngestor
from pipeline.frame_extraction import FrameExtractor
from pipeline.preprocessing import FramePreprocessor
from pipeline.prompt_engineering import PromptEngineer
from pipeline.vlm_inference import VLMInferencer
from pipeline.evaluation import Evaluator
from utils.jsonify import Jsonifier
from utils.logger import get_logger

logger = get_logger(__name__)
def run_pipeline(video_path, config):
    '''
    Run the pipeline for a given video and config.
    '''
    video = VideoIngestor(video_path).load()
    frames = FrameExtractor(config['num_frames']).extract(video)
    preprocessed_frames = FramePreprocessor(config['detail']).preprocess(frames)
    prompt = PromptEngineer(config['prompt_template']).build_prompt(preprocessed_frames)
    ai_caption = VLMInferencer(config['api_key'],
                               config['model'],
                               config['base_url']).infer(prompt, preprocessed_frames)
    # Optionally compare with human caption
    # Evaluator().compare(ai_caption, human_caption)
    return ai_caption
def main():
    '''
    Run the pipeline for all videos in the given directory.
    '''
    if len(sys.argv) < 3:
        print("Usage: video-describe <video_path> <config_path>")
        exit(1)
    video_path = sys.argv[1]
    config_path = sys.argv[2]
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    VIDEO_DIR = video_path
    json_handler = Jsonifier("video_metadata.json")
    logger.info("\n--- Searching for videos in '%s' directory ---",VIDEO_DIR)
    video_extensions = ["*.mp4", "*.mov", "*.avi", "*.mkv"]
    video_files = []

    for extension in video_extensions:
        video_files.extend(glob.glob(os.path.join(VIDEO_DIR, extension)))
    logger.info(f"Found {len(video_files)} videos:")

    for video_file in video_files:
        if json_handler.check_video_description_exists(video_file):
            logger.info("Skipping %s because it already has a description", video_file)
            continue

        logger.info("Running pipeline for %s", video_file)
        result = run_pipeline(video_file, config)
        if result:
            new_entry = {
                "file_path": video_file,
                "description": result
            }
            json_handler.json_entry(new_entry)
        else:
            logger.info("No result from pipeline for %s", video_file)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error("An error occurred: %s", e)
        sys.exit(1)