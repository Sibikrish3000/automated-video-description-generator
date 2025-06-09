from pipeline.ingestion import VideoIngestor
from pipeline.frame_extraction import FrameExtractor
from pipeline.preprocessing import FramePreprocessor
from pipeline.prompt_engineering import PromptEngineer
from pipeline.vlm_inference import VLMInferencer
from pipeline.evaluation import Evaluator
from utils.jsonify import json_entry
import json

import yaml

def run_pipeline(video_path, config):
    video = VideoIngestor(video_path).load()
    frames = FrameExtractor(config['num_frames']).extract(video_path)
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
    result = run_pipeline(video_path, config)
    if result:
        new_entry = {
            "file_path": video_path,
            "description": result
        }
        json_entry("video_metadata.json", new_entry)
    print(result)

if __name__ == "__main__":
    main()