from pipeline.ingestion import VideoIngestor
from pipeline.frame_extraction import FrameExtractor
from pipeline.preprocessing import FramePreprocessor
from pipeline.prompt_engineering import PromptEngineer
from pipeline.vlm_inference import VLMInferencer
from pipeline.evaluation import Evaluator
from utils.jsonify import Jsonifier
import glob
import yaml
import os

def run_pipeline(video_path, config):
    video = VideoIngestor(video_path).load()
    frames = FrameExtractor(config['num_frames']).extract(video)
    preprocessed_frames = FramePreprocessor(config['detail']).preprocess(frames)
    prompt = PromptEngineer(config['prompt_template']).build_prompt(preprocessed_frames)
    ai_caption = VLMInferencer(config['api_key'], config['model'], config['base_url']).infer(prompt, preprocessed_frames)
    # Optionally compare with human caption
    # Evaluator().compare(ai_caption, human_caption)
    return ai_caption
def main():
    import sys
    if len(sys.argv) < 3:
        print("Usage: python main.py <video_path> <config_path>")
        exit(1)
    video_path = sys.argv[1]
    config_path = sys.argv[2]
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    VIDEO_DIR = video_path
    json_handler = Jsonifier("video_metadata.json")
    print(f"\n--- Searching for videos in '{VIDEO_DIR}' directory ---")
    video_extensions = ["*.mp4", "*.mov", "*.avi", "*.mkv"]
    video_files = []

    for extension in video_extensions:
        video_files.extend(glob.glob(os.path.join(VIDEO_DIR, extension)))
    print(f"Found {len(video_files)} videos:")

    for video_file in video_files:
        if json_handler.check_video_description_exists(video_file):
            print(f"Skipping {video_file} because it already has a description")
            continue

        print(f"Running pipeline for {video_file}")
        result = run_pipeline(video_file, config)
        if result:
            new_entry = {
                "file_path": video_file,
                "description": result
            }
            json_handler.json_entry(new_entry)
        else:
            print(f"No result from pipeline for {video_file}")

if __name__ == "__main__":

    main()