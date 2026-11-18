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

# Split events into accepted and rejected based on the required fields
def validate_events(events):
    # Fields every event must have, filled in
    required_fields = ['event_id', 'occurred_at', 'user_id', 'name']

    rejected_count = 0
    accepted_count = 0
    accepted_events = []
    rejected_events = []

    for event in events:
        # True only if every required field exists and is not empty
        is_valid = all(event.get(field) for field in required_fields)

        if is_valid:
            accepted_count += 1
            accepted_events.append(event)
        else:
            # Missing event_id (or any other field): reject, never invent a value
            rejected_count += 1
            rejected_events.append(event)

    return rejected_count, accepted_count, accepted_events, rejected_events

# Convert each accepted event into a JSON line with keys in alphabetical order
def standardize_events(accepted_events):
    standardized_events = []

    for valid_event in accepted_events:
        # sort_keys=True: same key order every time; no indent: one event per line
        standardized_event = json.dumps(valid_event, sort_keys=True)
        standardized_events.append(standardized_event)

    return standardized_events

# Folder where the input files arrive
input_dir = "data/input/"
file_paths = list_input_files(input_dir)


for file_path in file_paths:
    events = load_events(file_path)
    rejected_count, accepted_count, accepted_events, rejected_events = validate_events(events)
    standardized_events = standardize_events(accepted_events)
    
print("rejected_count", rejected_count)
print("accepted_count", accepted_count)
print(standardize_events)