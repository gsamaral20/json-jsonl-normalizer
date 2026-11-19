# Imports
from functions import (
    list_input_files,
    load_events,
    validate_events,
    standardize_events,
    write_jsonl,
    build_and_export_summary,
    print_summary,
)

# Folder where the input files arrive
input_dir = "data/input/"

# Step 1: list the full path of every file in the input folder
file_paths = list_input_files(input_dir)

# Process one file at a time
for file_path in file_paths:
    # Step 2: read the file, detect the format (array or JSONL) and load the events
    events = load_events(file_path)

    # Step 3: split events into accepted and rejected (required fields check)
    rejected_count, accepted_count, accepted_events, rejected_events = validate_events(events)

    # Step 4: convert each accepted event into a JSON line with sorted keys
    standardized_events = standardize_events(accepted_events)

# Step 5: write the standardized events to the output JSONL (atomic write)
write_jsonl(standardized_events)

# Step 6: build the summary and export it to JSON
summary = build_and_export_summary(accepted_count, rejected_count)

# Step 7: print the summary in an executive format
print_summary(summary)