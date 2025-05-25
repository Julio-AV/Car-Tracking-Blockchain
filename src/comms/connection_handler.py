import socket
from threading import Lock
import threading
import queue
import logging
from typing import Union
from utils.IP_file_handler import read_connections_from_file
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
class ConnectionHandler:
    def __init__(self, IP: str ,port: int, queue_to_node: queue.Queue, queue_from_node: queue.Queue):
        self.queue_to_node = queue_to_node
        self.queue_from_node = queue_from_node
        self.port = port 
        self.IP = IP;
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("0.0.0.0", self.port)) #Bind socket to all interfaces
        self.server_socket.listen(5)
        self.connections_lock = Lock()
        self.open_connections = {}   #Dictionary that stores connections as {IP: socket}
        self.connections_to_open = read_connections_from_file(self.IP) #List of connections that the node should open once it starts

    def safe_close(self, client_addr: str) -> None:
        sock = self.open_connections[client_addr]
        with self.connections_lock:
            if not sock._closed:  # Comprueba si el socket ya está cerrado
                sock.close()

    def remove_connection(self, IP: str) -> None:
        with self.connections_lock:
            if IP in self.open_connections.keys():
                sock = self.open_connections[IP]
                if not sock._closed:
                    sock.close()
                del self.open_connections[IP]

    def accept_connection(self) -> Union[str, int]:
        with open("logs.txt", "a") as archivo:
                    archivo.write("Waiting to accept connection...\n")  # Escribir una línea
        client_socket, client_address = self.server_socket.accept()
        client_address: str = client_address[0] #We only need the IP
        with self.connections_lock:
            if client_address in self.open_connections.keys():
                client_socket.close()
            else:
                self.open_connections[client_address] = client_socket
                
                with open("logs.txt", "a") as archivo:
                    archivo.write(f"Connection accepted with {client_address}!\n")  # Escribir una línea
                return client_address
            print(f"connection stablished with {client_address}")
        return -1
    
    def open_connection(self, IP: str, port: int) -> None:
        with self.connections_lock:
            if IP not in self.open_connections:
                try:
                    logging.info(f"Trying to connect to {IP}")
                    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    #client_socket.settimeout(5)  # Set a timeout of 5 seconds (this timeout is applied to every aspect of the connection)
                    client_socket.connect((IP, port))
                    self.open_connections[IP] = client_socket
                    print(f"Connection established with {IP}")
                    self.launch(IP) #Listen to the connection

                except socket.timeout:
                    logging.error(f"Connection attempt to {IP} timed out.")
                except ConnectionRefusedError:
                    logging.error(f"Connection to {IP} was refused. The server may not be accepting connections.")
                except OSError as e:
                    logging.error(f"An error occurred while trying to connect to {IP}: {e}")
                except Exception as e:
                    logging.error(f"Unexpected error when connecting to {IP}: {e}")

            else:
                logging.warning(f"There is already an open connection with {IP}")

    def open_multiple_connections(self, IPs: list, ports = 5500):
        """
        Open multiple connections from a list
        """
        for IP in IPs:
            if IP != self.IP:
                logging.info(f"Opening connection with {IP}")
                
                self.open_connection(IP, ports)

    def listen_once(self,  client_ip: str, size: int = 8192):
        """
        This function listens to a socket once
        """
        client_socket = self.open_connections[client_ip]
        try:
            data = client_socket.recv(size)
            if data:
                #print(f"data received: {data.decode('utf-8')}")
                
                with open("logs.txt", "a") as archivo:
                    archivo.write("Data received!\n") 
                self.queue_to_node.put(data)   #No need to decode the data since our data_handler will do it
            else:
                print("Client closed connection.")
                self.remove_connection(client_ip)
        except ConnectionResetError:
            print("Connection was restarted by client, closing socket...")
            self.remove_connection(client_ip)

        except socket.timeout as e:
            print(e)
            print("Connection timed out while receiving data")

        except socket.error as e:
            if e.errno == 9:  # Errno 9: Bad file descriptor
                print("Socket closed. Exiting listener thread...")
            else:
                print(f"Error in socket: {e}")

            self.remove_connection(client_ip)
        except Exception as e:
            print(f"Unexpected error: {e}")
            self.remove_connection(client_ip)

    def listen(self, client_ip: str, size: int = 1024):
        """
        This function listen to a socket until it gets closed
        """
        while client_ip in self.open_connections.keys():
            self.listen_once(client_ip)
        logging.warning(f"Connection with {client_ip} was closed")


    def send(self, client_IP: str, msg: str) -> None:
        client_socket = self.open_connections[client_IP]
        encoded_msg = self.encode_msg(msg)
        client_socket.sendall(encoded_msg)
    
    def encode_msg(self, msg: str) -> bytes:
        
        return msg.encode()
    
    def consume_and_broadcast(self):
        """
        This function will be used by a thread that will listen to the queue between the node and the connection handler and will broadcast the messages to all open connections
        """
        while True:
            msg = self.queue_from_node.get()
            self.broadcast(msg)

    def broadcast(self, msg: str) -> None:
        """
        Send a message to all open sockets
        """
        encoded_msg = self.encode_msg(msg)
        for soc in self.open_connections.values():
            soc.sendall(encoded_msg)


    def start(self):
        """
        Start all threads from the connection handler
        """
        accepter = threading.Thread(target=self.accept_and_launch) #Thread to accept connections
        accepter.start()
        broadcaster = threading.Thread(target=self.consume_and_broadcast) # Thread that will listen to the queue and broadcast the messages
        broadcaster.start()
        for IP in self.connections_to_open:
            if IP != self.IP: #Avoid auto connection
                logging.info(f"Opening connection with {IP}")
                self.open_connection(IP, self.port)

    def launch(self, IP: str):
        """
        When the handler opens a connection, it will start a thread to listen to that connection
        """
        listener = threading.Thread(target=self.listen, args=(IP,))
        listener.start()
        
    def accept_and_launch(self):
        while True:
            ip = self.accept_connection() 
            if ip != -1:
                logging.info(f"Connection accepted with {ip}, launching listener")
                self.launch(ip)
