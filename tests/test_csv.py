import csv
import json
import os
CSV_FILE = "/home/julian/Vsocde/python_/celltron-multi-source-ingestion/multi-source-ingestion/Sample_Articles.csv"

OUTPUT_DIR = "/home/julian/Vsocde/python_/celltron-multi-source-ingestion/multi-source-ingestion/output"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "csv_sources.json")



ENCODINGS = ["utf-8", "latin-1", "cp1252", "iso-8859-1", "utf-16"]

def csv_to_json() -> bool:
    for encoding in ENCODINGS:
        try:
            with open(CSV_FILE, newline="", encoding=encoding) as csvfile:
                reader = csv.DictReader(csvfile)
                data = list(reader)

            with open(OUTPUT_FILE, "w", encoding="utf-8") as jsonfile:
                json.dump(data, jsonfile, indent=2, ensure_ascii=False)

            print(f"✓ Converted CSV → JSON using {encoding}")
            print(f"✓ Saved to {CSV_FILE}")
            return True

        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"❌ File not found: {CSV_FILE}")
            return False

    print("❌ Failed to read CSV with known encodings")
    return False


    
