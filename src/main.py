## Imports
import json
import os

# List the full path of every file in the input folder
def list_input_files(input_dir):
    # List the names of the files in the folder (names only, not full paths)
    file_names = os.listdir(input_dir)

    # Build the full path of each file
    file_paths = []
    for file_name in file_names:
        file_path = os.path.join(input_dir, file_name)
        file_paths.append(file_path)
    return file_paths

def load_events(file_path):
    # Read the whole file as text
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()

    # The first character that is not whitespace tells the format
    first_char = text.lstrip()[0]

    if first_char == "[":
        # JSON array: parse everything at once
        events = json.loads(text)
    else:
        # JSONL: one JSON object per line
        events = []
        for row in text.splitlines():
            # Skip empty lines
            if row.strip():
                events.append(json.loads(row))

    return events

# Folder where the input files arrive
input_dir = "data/input/"
file_paths = list_input_files(input_dir)


for file_path in file_paths:
    events = load_events(file_path)
    print("###########")
    print(events)