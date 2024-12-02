import connection_handler
import threading
import queue
class Node:
    def __init__(self,):
        """
        This queue is for the relation producer-consumer between the connection handler and the data_handler
        """
        self.port = 5500
        self.data_queue = queue.Queue
        self.connection_handler = connection_handler(self.port)