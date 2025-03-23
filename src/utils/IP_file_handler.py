import os
def write_list_to_csv(file_name, data_list):
    """
    Writes data from a list to a CSV file.

    Args:
        file_name (str): Name of the output CSV file.
        data_list (list): List of data to write. 
            Each element of the list should be a list or tuple.
    """
    try:
        with open(file_name, mode='w', newline='', encoding='utf-8') as csv_file:
            for data in data_list:
                csv_file.write(data+"\n")
        
        print(f"Data successfully written to {file_name}")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")


def read_list_from_csv(file_name):
    """
    Reads data from a CSV file line by line and returns a list of strings.

    Args:
        file_name (str): The name of the input CSV file.

    Returns:
        list: A list of strings, each representing a line in the file.
    """
    try:
        with open(file_name, mode='r', encoding='utf-8') as csv_file:
            # Read all lines and strip newline characters
            data_list = [line.strip() for line in csv_file]
        print(f"Data successfully read from {file_name}")
        return data_list
    except Exception as e:
        print(f"Error reading from CSV file: {e}")
        return []
    
def delete_file(file_name):
    """
    Deletes a file if it exists.

    Args:
        file_name (str): The name of the file to delete.
    """
    try:
        if os.path.exists(file_name):
            os.remove(file_name)
            print(f"File '{file_name}' successfully deleted.")
        else:
            print(f"File '{file_name}' does not exist.")
    except Exception as e:
        print(f"Error deleting file '{file_name}': {e}")


if __name__ == "__main__":
    data = [
        "Test_data_1",
        "Test_data_2"
    ]
    file_name = "Test_file.csv"
    write_list_to_csv(file_name, data)
    # Example usage
    data = read_list_from_csv(file_name)
    print(data)
    delete_file(file_name)
    