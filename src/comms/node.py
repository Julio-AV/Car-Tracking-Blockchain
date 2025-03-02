from connection_handler import ConnectionHandler
from data_handler import DataHandler
import queue
import multiprocessing
class Node:
    """
    This class works as a mediator between the connection_handler and the data_handler, connection_handler will use queue.Queue since connection_handler uses
    threading because it does plenty of I/O operation, and data_handler will use multiprocessing.Queue since data_handler uses multiprocessing because it does plenty of CPU operations
    """
    def __init__(self):
        self.port = 5500    #In case of deploying a docker container, this port needs to be the same that you openned in the container
        self.queue_to_connectionHandler = queue.Queue()   #Queue between node and ConnectionHandler (ConnectionHandler is the producer, and node is the consumer)
        self.queue_from_connectionHandler = queue.Queue() #Queue between node and ConnectionHandler (Node is the producer, and ConnectionHandler is the consumer)
        self.connection_handler = ConnectionHandler(self.port, self.queue_from_connectionHandler, self.queue_to_connectionHandler)
        self.queue_to_dataHandler = multiprocessing.Queue() #Queue between node and dataHandler (dataHandler is the producer, and node is the consumer)
        self.queue_from_dataHandler = multiprocessing.Queue() #Queue between node and dataHandler (Node is the producer, and dataHandler is the consumer)
        self.data_handler = DataHandler(self.queue_from_dataHandler, self.queue_to_dataHandler)
        #TODO: start connection_handler and data_handler
    
