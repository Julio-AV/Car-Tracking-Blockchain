from .connection_handler import ConnectionHandler
from .data_handler import DataHandler
from utils.key_handler import load_keys, load_node_name, load_node_IP
import queue
import multiprocessing
import threading
import time
class Node:
    """
    This class works as a mediator between the connection_handler and the data_handler, connection_handler will use queue.Queue since connection_handler uses
    threading because it does plenty of I/O operation, and data_handler will use multiprocessing.Queue since data_handler uses multiprocessing because it does plenty of CPU operations
    """
    def __init__(self):
        
        self.name = load_node_name() #Name of the node, e.g. DGT-1
        self.IP = load_node_IP() #IP of the node
        self.public_keys, self.private_key = load_keys(self.name) #Public keys and private key from a node
        self.port = 5500    #In case of deploying a docker container, this port needs to be the same that you openned in the container
        
        self.queue_to_connectionHandler = queue.Queue()   #Queue between node and ConnectionHandler (ConnectionHandler is the producer, and node is the consumer)
        self.queue_from_connectionHandler = queue.Queue() #Queue between node and ConnectionHandler (Node is the producer, and ConnectionHandler is the consumer)
        self.connection_handler = ConnectionHandler(self.IP, self.port, self.queue_from_connectionHandler, self.queue_to_connectionHandler)
        self.queue_to_dataHandler = multiprocessing.Queue() #Queue between node and dataHandler (dataHandler is the producer, and node is the consumer)
        self.queue_from_dataHandler = multiprocessing.Queue() #Queue between node and dataHandler (Node is the producer, and dataHandler is the consumer)
        self.process_manager = multiprocessing.Manager() #Manager to share data between processes
        self.transaction_list = self.process_manager.list() #List of transactions, this will be shared between node and data handler
        self.blockchain = self.process_manager.list() #Blockchain, this will be shared between node and data handler
        self.data_handler = DataHandler(self.queue_to_dataHandler, self.queue_from_dataHandler, self.public_keys, self.blockchain, self.transaction_list)
        print(f"Node {self.name} started successfully")
    
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

    def operate(self):
        """
        Generate data to be sent to the network, this function will be overriden by simulation scenarios nodes
        """
        pass

    def start(self):
        """
        Start all node processes
        """
        thread_to_be_waited = threading.Thread(target=self.send) #We store it in a variable so the main thread waits infinitely for it
        thread_to_be_waited.start() #Start the thread
        threading.Thread(target=self.receive).start()
        self.connection_handler.start()
        self.data_handler.start()
        time.sleep(2) #Give time for the connection handler and data handler to start
        threading.Thread(target=self.operate).start()
        thread_to_be_waited.join() #Wait for the thread to finish (infinite waiting)

    def _clear_transaction_list(self):
        """
        Clear the transaction list, this is used to clear the transaction list after a block is created
        """
        self.transaction_list[:] = []