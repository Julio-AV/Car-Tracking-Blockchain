from connection_handler import ConnectionHandler
import queue
import multiprocessing
class Node:
    """
    This class works as a mediator between the connection_handler and the data_handler
    """
    def __init__(self):
        self.port = 5500    #In case of deploying a docker container, this port needs to be the same that you openned in the container
        self.data_queue = queue.Queue   #Queue between node and ConnectionHandler (ConnectionHandler is the producer, and node is the consumer)
        self.connection_handler = ConnectionHandler(self.port, )