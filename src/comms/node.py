import connection_handler
import queue
class Node:
    def __init__(self,):
        self.port = 5500    #In case of deploying a docker container, this port needs to be the same that you openned in the container
        self.data_queue = queue.Queue   #Producer-consumer queue between connection_handler and data_handler
        self.connection_handler = connection_handler(self.port)