import json
import os
class Jsonifier:
    def __init__(self, json_path):
        self.json_path = json_path

    def json_entry(self, new_entry):
        """
        Updates or creates a JSON file with the structure:
        {
        "path/to/filename.extension": {
            "file_path": "...",
            "description": "..."
        },
        ...
        }
        """
        # Load existing JSON or create empty
        if os.path.exists(self.json_path):
            try:
                with open(self.json_path, 'r') as f:
                    data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        else:
            data = {}

        # Extract key and update
        file_path = new_entry.get("file_path")
        if not file_path:
            raise ValueError("Missing 'file_path' in new_entry")

        data[file_path] = new_entry

        # Save to file
        with open(self.json_path, 'w',) as f:
            json.dump(data, f, indent=4)

        print(f"description added: {file_path}")
    def check_video_description_exists(self, file_path):
        if os.path.exists(self.json_path):
            with open(self.json_path, 'r') as f:
                data = json.load(f)
                return file_path in data and data[file_path]["description"] is not None
        return False
