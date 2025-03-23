from .connection_handler import ConnectionHandler
from .data_handler import DataHandler
from scenarios.key_handler import load_keys, load_node_name
import queue
import multiprocessing
import threading
class Node:
    """
    This class works as a mediator between the connection_handler and the data_handler, connection_handler will use queue.Queue since connection_handler uses
    threading because it does plenty of I/O operation, and data_handler will use multiprocessing.Queue since data_handler uses multiprocessing because it does plenty of CPU operations
    """
    def __init__(self):
        self.name = load_node_name() #Name of the node, e.g. DGT-1
        self.port = 5500    #In case of deploying a docker container, this port needs to be the same that you openned in the container
        self.blockchain = [] #List of blocks
        self.public_keys, self.private_key = load_keys(self.name) #Public keys and private key from a node
        self.queue_to_connectionHandler = queue.Queue()   #Queue between node and ConnectionHandler (ConnectionHandler is the producer, and node is the consumer)
        self.queue_from_connectionHandler = queue.Queue() #Queue between node and ConnectionHandler (Node is the producer, and ConnectionHandler is the consumer)
        self.connection_handler = ConnectionHandler(self.port, self.queue_from_connectionHandler, self.queue_to_connectionHandler)
        self.queue_to_dataHandler = multiprocessing.Queue() #Queue between node and dataHandler (dataHandler is the producer, and node is the consumer)
        self.queue_from_dataHandler = multiprocessing.Queue() #Queue between node and dataHandler (Node is the producer, and dataHandler is the consumer)
        self.data_handler = DataHandler(self.queue_to_dataHandler, self.queue_from_dataHandler, self.public_keys, self.blockchain)
        self.connection_handler.start()
        self.data_handler.start()
    
    def send(self):
        """
        Send a message to the connection handler from the data handler
        """
        while True:
            data_to_send = self.queue_from_dataHandler.get()
            self.queue_to_connectionHandler.put(data_to_send)
    
    def receive(self):
        """
        Send a message to the data handler from the connection handler
        """
        while True:
            data_to_send = self.queue_from_connectionHandler.get()
            self.queue_to_dataHandler.put(data_to_send)

    def start(self):
        """
        Start both node processes
        """
        threading.Thread(target=self.send).start()
        threading.Thread(target=self.receive).start()


