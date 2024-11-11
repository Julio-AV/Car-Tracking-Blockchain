import socket
class server:
    def __init__(self, port, IP = "0.0.0.0"):
        self.port = port 
        self.IP = IP;
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.port))
        self.server_socket.listen()
        self.open_connections = {}   #Hashmap where we will store out connections

    def accept_connection(self):
        client_socket, client_address = self.server_socket.accept()
        self.open_connections[client_address] = client_socket
        print(f"connection stablished with {client_address}")


    def listen(self, client_socket, client_ip, size = 1024):
        try:
            data = client_socket.recv(size)
            if data:
                print(f"data received: {data.decode('utf-8')}")
                return data
            else:
                print("Client closed connection.")
                client_socket.close()
                del self.open_connections[client_ip]
        except ConnectionResetError:
            print("Connection was restarted by client, closing socket...")
            client_socket.close()
            del self.open_connections[client_ip]

        except socket.timeout:
            print("Connection timed out while receiving data")

        except socket.error as e:
            print(f"Error in socket: {e}")
            client_socket.close()
            del self.open_connections[client_ip]
        except Exception as e:
            print(f"Unexpected error: {e}")
            client_socket.close()
            del self.open_connections[client_ip]
        return -1


    def send(self, client_socket, msg):
        client_socket.sendall(msg)


            
