"""
This class is in charge of accepting and refusing data transfers
"""
import queue

class Data_handler:
    def __init__(self, data_queue: queue.Queue ):
        self.data_queue = data_queue