import csv
import json
import os


class CSVToJSON:
    ENCODINGS = ["utf-8", "latin-1", "cp1252", "iso-8859-1", "utf-16"]

    def __init__(self, csv_file: str, required_columns=None):
        self.csv_file = csv_file
        self.required_columns = required_columns or []
        self.data = []

    def _validate_file(self):
        if not os.path.exists(self.csv_file):
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")

        if os.path.getsize(self.csv_file) == 0:
            raise ValueError("CSV file is empty")

    def _validate_columns(self, fieldnames):
        if not fieldnames:
            raise ValueError("CSV file has no header row")

        missing = [col for col in self.required_columns if col not in fieldnames]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    def read_csv(self) -> list:
        """Read CSV and return data as list of dictionaries"""
        try:
            self._validate_file()
        except Exception as e:
            print(f"❌ {e}")
            return []

        for encoding in self.ENCODINGS:
            try:
                with open(self.csv_file, newline="", encoding=encoding) as csvfile:
                    reader = csv.DictReader(csvfile)
                    
                    self._validate_columns(reader.fieldnames)
                    
                    data = []
                    for row in reader:
                        if not any(row.values()):
                            continue  # skip empty rows
                        
                        row["source"] = "csv"
                        data.append(row)
                
                if not data:
                    raise ValueError("CSV contains no valid data rows")
                
                self.data = data
                print(f"✓ CSV read successfully using {encoding}")
                print(f"✓ Found {len(data)} records")
                return data
                
            except UnicodeDecodeError:
                continue  # try next encoding
            except Exception as e:
                print(f"❌ Error processing CSV: {e}")
                return []
        
        print("❌ Failed to decode CSV with known encodings")
        return []

    def convert(self) -> list:
        """Main method to convert CSV to data (no saving)"""
        data = self.read_csv()
        return data
