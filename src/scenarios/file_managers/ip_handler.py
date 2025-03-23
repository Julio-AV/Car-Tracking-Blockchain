import csv
import os
def read_IPs_csv(file_path = "data/IPs.csv"):
    """Reads a CSV file and returns a list of its rows."""
    data = []
    with open(file_path, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            data.append(row)
    return data

def write_IPs_csv(data, file_path = "data/IPs.csv"):
    """Writes a list of data to a CSV file."""
    with open(file_path, mode='w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(data)

def clear_IPs_files(file_path = "data/IPs.csv"):
    try:
        if os.path.exists(file_path):
            os.remove(file_path) 
    except Exception as e:
        print(f"Error deleting IPs file {file_path}: {e}")
