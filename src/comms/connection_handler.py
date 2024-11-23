import socket
from threading import Lock
class Connection_handler:
    def __init__(self, port: int, IP: str = "0.0.0.0"):
        self.port = port 
        self.IP = IP;
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.port))
        self.server_socket.listen()
        self.connections_lock = Lock()
        self.open_connections = {}   #Hashmap where we will store connections as {IP: socket}

    def safe_close(self, sock):
        with self.connections_lock:
            if not sock._closed:  # Comprueba si el socket ya está cerrado
                sock.close()
    def remove_connection(self, IP):
        with self.connections_lock:
            del self.open_connections[IP]

    def accept_connection(self):
        client_socket, client_address = self.server_socket.accept()
        with self.connections_lock:
            if client_address in self.open_connections.keys():
                client_socket.close()
                return -1
            else:
                self.open_connections[client_address] = client_socket
                print(f"connection stablished with {client_address}")
                return client_address

    def open_connection(self, IP, port):
        with self.connections_lock:
            if IP not in self.open_connections.keys():
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((IP, port))
                self.open_connections[IP] = client_socket
                print(f"connection stablished with {IP}")
            else:
                print(f"There is already an open connection with {IP}")


    def listen(self,  client_ip, size = 1024):
        
        client_socket = self.open_connections[client_ip]
        try:
            data = client_socket.recv(size)
            if data:
                print(f"data received: {data.decode('utf-8')}")
                return data
            else:
                print("Client closed connection.")
                self.safe_close(client_socket)
                self.remove_connection(client_ip)
        except ConnectionResetError:
            print("Connection was restarted by client, closing socket...")
            self.safe_close(client_socket)
            self.remove_connection(client_ip)

        except socket.timeout:
            print("Connection timed out while receiving data")

        except socket.error as e:
            print(f"Error in socket: {e}")
            self.safe_close(client_socket)
            self.remove_connection(client_ip)
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.safe_close(client_socket)
            self.remove_connection(client_ip)
        return -1


    def send(self, client_IP, msg):
        client_socket = self.open_connections[client_IP]
        client_socket.sendall(msg.encode())
    
    def encode_msg(self, msg):
        """
        TODO: Encoding to JSON or whatever type of communication will be using
        """
        pass

    def broadcast(self, msg):
        msg = msg.encode()
        for soc in self.open_connections.values():
            soc.sendall(msg)


            
