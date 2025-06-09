import json
import os

def json_entry(json_path, new_entry):
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
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as f:
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
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    print(f"Added/Updated: {file_path}")
