import os
import random
import json

def write_connections_to_file(connections: dict, file_name="data/connections.json"):
    """
    Writes the connections dictionary to a file in JSON format.

    Args:
        connections (dict): A dictionary where keys are IP addresses and values are lists of connected IP addresses.
        file_name (str): The name of the output file.
    """
    try:
        with open(file_name, mode='w', encoding='utf-8') as file:
            json.dump(connections, file, indent=4)
        print(f"Connections successfully written to {file_name}")
    except Exception as e:
        print(f"Error writing to file: {e}")


def read_connections_from_file(IP, file_name="data/connections.json"):
    """
    Reads the connections from a file in JSON format.

    Args:
        IP (str): The IP address to look for in the connections.
        file_name (str): The name of the input file.

    Returns:
        list: A list of connected IP addresses.
    """
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            connections = json.load(file)
            return connections.get(IP)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding JSON from {file_name}.")
        return []
    
def delete_connections_file(file_name = "data/connections.json"):
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





def generate_connected_network(ips):
    """
    Generates a random network of connected IP addresses. 
    The graph generated has a connected component of 1.
    """
    if len(ips) < 2:
        return {ip: [] for ip in ips}

    connections = {ip: [] for ip in ips}
    connected = [ips[0]]
    not_connected = set(ips[1:])

    # Step 1: Make sure the graph is connected (minimum spanning tree idea)
    while not_connected:
        a = random.choice(connected)
        b = random.choice(list(not_connected))

        connections[a].append(b)
        connections[b].append(a)

        connected.append(b)
        not_connected.remove(b)

    # Step 2 (optional): Add some extra edges without making it fully connected
    possible_edges = [
        (a, b) for i, a in enumerate(ips) for b in ips[i+1:]
        if b not in connections[a]
    ]

    random.shuffle(possible_edges)
    extras = random.randint(0, len(ips) // 2)

    for a, b in possible_edges[:extras]:
        connections[a].append(b)
        connections[b].append(a)

    return connections

if __name__ == "__main__":
    # data = [
    #     "Test_data_1",
    #     "Test_data_2"
    # ]
    # file_name = "Test_file.csv"
    # write_list_to_csv(file_name, data)
    # # Example usage
    # data = read_list_from_csv(file_name)
    # print(data)
    # delete_file(file_name)
    ips = [
    "192.168.0.1",
    "192.168.0.2",
    "192.168.0.3",
    "192.168.0.4",
    "192.168.0.5"
    ]

    network = generate_connected_network(ips)
    for ip, neighbors in network.items():
        print(f"{ip}: {neighbors}")

    