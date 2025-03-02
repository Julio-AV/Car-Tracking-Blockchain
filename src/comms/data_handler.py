"""
This class is in charge of accepting and refusing data transfers, it will have to check weather the sender is allowed to send data to the receiver, the transaction validation is done in transactions.
"""
import queue
import multiprocessing
from blockchain.transactionFactory import TransactionFactory
import json
class DataHandler:
    def __init__(self, queue_from_node: multiprocessing.Queue, queue_to_node: multiprocessing.Queue, keys: dict):
        """
        Connection handler is in charge of telling the connection_handler whether to broadcast a transaction or a block again, therefore to know whether my transaction has 
        been accepted by the network, I will have to receive my transaction again from the network.

        It is also in charge of validating data from the network and building the blockchain
        """
        self.queue_from_node = queue_from_node
        self.queue_to_node = queue_to_node
        self.keys = keys #Key dictionary with validator: public key
        self.transaction_list = [] #This list will contain all the transactions that have been validated and received throught the network

        def run(self):
            """
            This function will star the data handler
            """
            multiprocessing.Process(target=self.).start()

        def consume_queue():
            """
            Main function of the data handler, it will consume the queue from the node, validate the transactions and decide whether to send them back to the network or not
            TODO: Parse the information received from the network, if it contains a header field and a transactions field, it means it's a block
            """
            while True:
                received_data = self.queue_from_node.get()
                try: 
                    json_data = json.loads(received_data)
                except json.JSONDecodeError:
                    print("Data received was not in JSON format")
                    continue
                if "header" in json_data and "transactions" in json_data.keys():
                    #if it contains a header field and a transactions field, it means it's a block
                    #TODO: Create the block
                else:
                    #TODO: Create the transaction



                


        def validate_transaction(self, transaction: str):
            """
            This function will accept a transaction from the network and validate it
            """
            transaction = TransactionFactory.create_transaction(transaction)
            if not transaction:
                #If the transaction factory could not recover transaction, return
                print("Transaction was discarded")
                return
            transaction.
            self.transaction_list.append(transaction)
            self.queue_to_node.put(transaction)