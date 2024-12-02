import csv

# Utility: Load CSV file into a list of dictionaries
def load_csv(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            return [row for row in reader]
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return []
    except Exception as e:
        print(f"Error reading file {filepath}: {e}")
        return []


