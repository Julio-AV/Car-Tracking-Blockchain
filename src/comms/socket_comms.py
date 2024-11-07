"""
Library with socket connections used for the blockchain
"""
import json
import socket

def open_connection(ip: str, port: int):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((ip, port))
        print(f"Connection with {ip}:{port} was successful")
        return sock
    
    except socket.error as e:
        print(f"Error connecting with {ip}:{port} - {e}")
        return -1
    
def open_server_socket(ip: str, port: int, num_connections = 5):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(num_connections)
        print(f"Server listening in {ip}:{port}")
        return server
    
    except socket.error as e:
        print(f"Error starting connection server {ip}:{port} - {e}")
        return None