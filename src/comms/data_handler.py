"""
This class is in charge of accepting and refusing data transfers, it will have to check weather the sender is allowed to send data to the receiver, the transaction validation is done in transactions.
"""
import queue
import multiprocessing
class DataHandler:
    def __init__(self, queue_from_node: multiprocessing.Queue, queue_to_node: multiprocessing.Queue):
        self.queue_from_node = queue_from_node
        self.queue_to_node = queue_to_node