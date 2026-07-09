import os
import json

OUTPUT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "outputs"))

def ensure_output_dir():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def get_filepath(filename: str) -> str:
    ensure_output_dir()
    # Normalize name to prevent directory traversal
    basename = os.path.basename(filename)
    return os.path.join(OUTPUT_DIR, basename)

def read_json(filename: str):
    path = get_filepath(filename)
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error reading JSON from {path}: {e}")
        return None

def write_json(filename: str, data) -> str:
    path = get_filepath(filename)
    # Ensure nested subdirectories like generated_scripts/ exist if filename has them
    dir_path = os.path.dirname(os.path.join(OUTPUT_DIR, filename))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    path = os.path.join(OUTPUT_DIR, filename)
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        return path
    except Exception as e:
        print(f"Error writing JSON to {path}: {e}")
        raise e

def write_text(filename: str, text: str) -> str:
    path = os.path.join(OUTPUT_DIR, filename)
    dir_path = os.path.dirname(path)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)
        return path
    except Exception as e:
        print(f"Error writing text to {path}: {e}")
        raise e
