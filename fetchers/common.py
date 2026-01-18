import os
import json

import os
import json

def save_to_json(new_data: list, output_file: str) -> bool:
    """
    Append new data to an existing JSON file.
    Creates the file if it does not exist.
    """

    if not new_data:
        print("❌ No data to save")
        return False

    try:
        # Load existing data if file exists
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                try:
                    existing_data = json.load(f)
                except json.JSONDecodeError:
                    existing_data = []
        else:
            existing_data = []

        # Ensure existing data is a list
        if not isinstance(existing_data, list):
            print("⚠ Existing JSON is not a list, resetting file")
            existing_data = []

        # Append new data
        merged_data = existing_data + new_data

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        # Save merged data
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(merged_data, f, indent=2, ensure_ascii=False)

        print(f"✓ Appended {len(new_data)} records (total: {len(merged_data)})")
        return True

    except Exception as e:
        print(f"❌ Error saving JSON: {e}")
        return False
