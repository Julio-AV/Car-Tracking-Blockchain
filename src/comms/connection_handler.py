import socket
from threading import Lock
import threading
import queue
import logging
from typing import Union
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
class Connection_handler:
    def __init__(self, port: int, data_queue: queue.Queue, IP: str = "0.0.0.0"):
        self.data_queue = data_queue
        self.port = port 
        self.IP = IP;
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.IP, self.port))
        self.server_socket.listen(5)
        self.connections_lock = Lock()
        self.open_connections = {}   #Dictionary that stores connections as {IP: socket}

    def safe_close(self, sock: socket.socket) -> None:
        with self.connections_lock:
            if not sock._closed:  # Comprueba si el socket ya está cerrado
                sock.close()
    def remove_connection(self, IP: str) -> None:
        with self.connections_lock:
            del self.open_connections[IP]

    def accept_connection(self) -> Union[str, int]:
        with open("mi_archivo.txt", "a") as archivo:
                    archivo.write("Waiting to accept connection...\n")  # Escribir una línea
        client_socket, client_address = self.server_socket.accept()
        client_address: str = client_address[0] #We only need the IP
        with self.connections_lock:
            if client_address in self.open_connections.keys():
                client_socket.close()
            else:
                self.open_connections[client_address] = client_socket
                
                with open("mi_archivo.txt", "a") as archivo:
                    archivo.write(f"Connection accepted with {client_address}!\n")  # Escribir una línea
                return client_address
            print(f"connection stablished with {client_address}")
        return -1
    
    def open_connection(self, IP: str, port: int) -> None:
        with self.connections_lock:
            if IP not in self.open_connections.keys():
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((IP, port))
                self.open_connections[IP] = client_socket
                print(f"connection stablished with {IP}")
            else:
                logging.warning(f"There is already an open connection with {IP}")


    def listen(self,  client_ip: str, size: int = 1024):
        """
        This function listens to a socket until it is closed
        """
        client_socket = self.open_connections[client_ip]
        try:
            while client_ip in self.open_connections.keys():
                data = client_socket.recv(size)
                if data:
                    print(f"data received: {data.decode('utf-8')}")
                    self.data_queue.put(data)   #No need to decode the data since our data_handler will do it
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


    def send(self, client_IP: str, msg: str) -> None:
        client_socket = self.open_connections[client_IP]
        encoded_msg = self.encode_msg(msg)
        client_socket.sendall(encoded_msg)
    
    def encode_msg(self, msg: str) -> bytes:
        """
        TODO: Encoding to JSON or whatever type of communication will be using
        """
        return msg.encode()

    def broadcast(self, msg: str) -> None:
        encoded_msg = self.encode_msg(msg)
        for soc in self.open_connections.values():
            soc.sendall(encoded_msg)


    def start(self):
        """
        When the handler opens a connection, it will start a thread to listen to that connection
        """
        accepter = threading.Thread(target=self.accept_and_launch)
        accepter.start()
        with open("mi_archivo.txt", "w") as archivo:
                    archivo.write("Thread launched to accept_and_lauch\n")  # Escribir una línea
        

    def accept_and_launch(self):
        #while True:
        ip = self.accept_connection() 
        if ip != -1:
            listener = threading.Thread(target=self.listen, args=(ip,))
            listener.start()
            # Abrir un archivo en modo escritura ('w')
            with open("mi_archivo.txt", "a") as archivo:
                archivo.write(f"launched listener to ip {ip}\n")  # Escribir una línea

