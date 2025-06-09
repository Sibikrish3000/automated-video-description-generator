# Automated Video Description Generator

A modular, extensible pipeline for generating natural language descriptions of videos using state-of-the-art Vision-Language Models (VLMs). This project is designed for research, prototyping, and practical applications in video understanding, accessibility, and content summarization.

---

## Features
- **Frame Extraction:** Evenly samples frames from videos for efficient and representative analysis.
- **Vision-Language Model Integration:** Supports OpenAI GPT-4o and compatible VLMs via API.
- **Prompt Engineering:** Customizable prompts to guide the model's output.
- **Batch Processing:** Processes all videos in a directory, skipping those already described.
- **Extensible Pipeline:** Modular design for easy customization and extension.
- **Logging & JSON Output:** Stores results in a JSON file for further analysis or integration.

---

## Directory Structure
```
.
├── main.py
├── config.yaml
├── requirements.txt
├── pyproject.toml
├── README.md
├── pipeline/
│   ├── ingestion.py
│   ├── frame_extraction.py
│   ├── preprocessing.py
│   ├── prompt_engineering.py
│   ├── vlm_inference.py
│   ├── evaluation.py
│   └── __init__.py
├── utils/
│   ├── logger.py
│   └── jsonify.py
├── tests/
│   └── test_pipeline.py
└── video_metadata.json
```

---

## Setup

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd automated-video-description-generator
   ```

2. **Create and activate a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## Configuration

Edit `config.yaml` to set your preferences and API credentials:

```yaml
num_frames: 10                # Number of frames to sample per video
detail: "high"                # Frame resolution: "low" (512x512) or "high" (1024x1024)
model: "gpt-4o"               # Model name (e.g., "gpt-4o" for OpenAI, or compatible VLM)
prompt_template: |
  You are a video analysis expert. These are sequential frames from a video. Please provide a single-paragraph description that covers the setting, main subjects, their actions, and the overall mood or narrative.
api_key: "YOUR_OPENAI_API_KEY" # Your API key for the VLM provider
base_url: "https://api.openai.com/v1" # API base URL (default for OpenAI)
```

---

## Usage

### **Batch Process a Directory of Videos**

Place your videos in a directory (e.g., `video/`). Supported formats: `.mp4`, `.avi`, `.mov`, `.mkv`.

Run the pipeline:
```sh
python main.py video/ config.yaml
```
- The script will process all videos in the directory, skipping those already described in `video_metadata.json`.
- Descriptions are saved in `video_metadata.json`.

### **Single Video Example**

To process a single video, you can modify `main.py` or call `run_pipeline(video_path, config)` directly in a script or notebook.

---

## Architecture Overview

- **main.py:** Orchestrates the pipeline, batch processes videos, and manages JSON output.
- **pipeline/ingestion.py:** Validates and loads video files.
- **pipeline/frame_extraction.py:** Extracts evenly spaced frames using OpenCV and PIL.
- **pipeline/preprocessing.py:** Resizes and normalizes frames.
- **pipeline/prompt_engineering.py:** Builds prompts for the VLM.
- **pipeline/vlm_inference.py:** Handles API calls to the VLM (e.g., OpenAI GPT-4o).
- **pipeline/evaluation.py:** (Optional) Compare AI and human captions.
- **utils/logger.py:** Standardized logging utility.
- **utils/jsonify.py:** Handles JSON output and duplicate checking.

---

## Extending the Pipeline
- **Add new frame selection strategies** (e.g., scene detection) in `frame_extraction.py`.
- **Swap or add VLM providers** by extending `vlm_inference.py`.
- **Customize prompts** in `config.yaml` or `prompt_engineering.py`.
- **Integrate evaluation metrics** in `evaluation.py`.

---

## Troubleshooting
- **Linter warning for `cv2.VideoCapture`:** This is a false positive; the code is correct and the warning is safely suppressed.
- **Module import errors:** Always run the pipeline from the project root (e.g., `python main.py ...`).
- **API errors:** Ensure your API key, model, and base URL are correct and you have access to the specified model.

---

## License
MIT License


