import socket
from threading import Lock
class server:
    def __init__(self, port, IP = "0.0.0.0"):
        self.port = port 
        self.IP = IP;
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.port))
        self.server_socket.listen()
        self.connections_lock = Lock()
        self.open_connections = {}   #Hashmap where we will store connections as {IP: socket}


    def add_connection(self, IP, socket):
        with self.connections_lock:
            self.open_connections[IP] = socket
    def remove_connection(self, IP):
        with self.connections_lock:
            del self.open_connections[IP]

    def accept_connection(self):
        client_socket, client_address = self.server_socket.accept()
        self.add_connection(client_address, client_socket)
        print(f"connection stablished with {client_address}")

    def open_connection(self, IP, port):
        if IP not in self.open_connection.keys():
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((IP, port))
            self.open_connection[IP] = client_socket
            print(f"connection stablished with {IP}")
        else:
            print(f"There is already an open connection with ")


    def listen(self, client_socket, client_ip, size = 1024):
        try:
            data = client_socket.recv(size)
            if data:
                print(f"data received: {data.decode('utf-8')}")
                return data
            else:
                print("Client closed connection.")
                client_socket.close()
                self.remove_connection(client_ip)
        except ConnectionResetError:
            print("Connection was restarted by client, closing socket...")
            client_socket.close()
            self.remove_connection(client_ip)

        except socket.timeout:
            print("Connection timed out while receiving data")

        except socket.error as e:
            print(f"Error in socket: {e}")
            client_socket.close()
            self.remove_connection(client_ip)
        except Exception as e:
            print(f"Unexpected error: {e}")
            client_socket.close()
            self.remove_connection(client_ip)
        return -1


    def send(self, client_socket, msg):
        client_socket.sendall(msg)


            
