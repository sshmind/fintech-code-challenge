import csv

def read_csv_file(file_path: str):
    with open(file_path, 'r') as file:
        
        csv_reader = csv.reader(file)
        next(csv_reader) # Skip headers

        data = list(csv_reader)  # Read all rows into a list

    return data
