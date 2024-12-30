"""
This class is in charge of accepting and refusing data transfers, it will have to check weather the sender is allowed to send data to the receiver, the transaction validation is done in transactions.
"""
import queue

class Data_handler:
    def __init__(self, data_queue: queue.Queue ):
        self.data_queue = data_queue
