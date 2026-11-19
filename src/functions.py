## Imports
import json
import os
from tempfile import NamedTemporaryFile

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

# Write the standardized events to a JSONL file using an atomic write
def write_jsonl(standardized_events):
    # Fixed destination of the final file
    destination = "data/output/events.jsonl"

    # Temporary file in the same folder as the final file
    output_dir = os.path.dirname(destination)

    with NamedTemporaryFile(mode="wt", encoding="utf-8", dir=output_dir, delete=False) as f:
        # One event per line
        for event in standardized_events:
            f.write(event + "\n")

    # File is closed: swap the temporary for the final file in one step
    os.replace(f.name, destination)

# Build the summary dictionary with the event counts and export it to JSON
def build_and_export_summary(accepted_count, rejected_count):
    summary = {
        # Every event that was read, accepted or not
        "events_read": accepted_count + rejected_count,
        "events_accepted": accepted_count,
        "events_rejected": rejected_count,
        # Rejected events always fail the same check: a required field is missing
        "rejection_reason": "missing fields",
    }

    # Where the summary file is written
    output_path = "data/output/summary.json"

    # "w" creates the file or overwrites it
    with open(output_path, "w", encoding="utf-8") as f:
        # indent=4: nested levels are indented by 4 spaces, one item per line (readable file)
        # ensure_ascii=False: keeps accented characters as they are instead of \uXXXX codes
        json.dump(summary, f, indent=4, ensure_ascii=False)

    return summary

# Print the summary in an executive format
def print_summary(summary):
    print("=" * 40)
    print("   EVENT NORMALIZATION REPORT")
    print("=" * 40)
    print(f"Events read      : {summary['events_read']}")
    print(f"Events accepted  : {summary['events_accepted']}")
    print(f"Events rejected  : {summary['events_rejected']}")
    print("-" * 40)
    print(f"Rejection reason : {summary['rejection_reason']}")
    print("=" * 40)