"""
This class is in charge of accepting and refusing data transfers, it will have to check weather the sender is allowed to send data to the receiver, the transaction validation is done in transactions.
"""
import queue
import multiprocessing
from blockchain.transactionFactory import TransactionFactory
import json
from blockchain.structure.transaction import Transaction
from blockchain.structure.block import Block
from .node import Node
class DataHandler:
    def __init__(self, queue_from_node: multiprocessing.Queue, queue_to_node: multiprocessing.Queue, public_keys: dict, node: Node):
        """
        Connection handler is in charge of telling the connection_handler whether to broadcast a transaction or a block again, therefore to know whether my transaction has 
        been accepted by the network, I will have to receive my transaction again from the network.

        It is also in charge of validating data from the network and building the blockchain
        """
        self.queue_from_node = queue_from_node
        self.queue_to_node = queue_to_node
        self.public_keys = public_keys #Key dictionary with validator: public key
        self.transaction_list = [] #This list will contain all the transactions that have been validated and received throught the network
        self.node = node

    def start(self):
        """
        This function will start the data handler
        """
        multiprocessing.Process(target=self.consume_queue).start()

    def consume_queue(self):
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
                #TODO: Create the block and add it to node if not in blockchain
                block = TransactionFactory.create_block(received_data)
                if block is None:
                    print("Block was discaraded")
                    #If block could not be recovered, or was discarded, continue
                    continue
            else:
                transaction = TransactionFactory.create_transaction(transaction)
                if transaction is None:
                    print("Transaction was discaraded")
                    #If transaction could not be recovered, or was discarded, continue
                    continue
                elif transaction in self.transaction_list:
                    print("Transaction was already received")
                    #If transaction was already received, continue
                    continue
                    
            
                is_valid = self.validate_transaction(transaction)
                if is_valid:
                    #If the transaction is valid, add it to the transaction list and the queue to node
                    self.transaction_list.append(transaction)
                    self.queue_to_node.put(transaction.serialize())
                else:
                    print(f"Transaction {transaction} was not valid")


                


    def validate_transaction(self, transaction: Transaction):
        """
        This function will accept a transaction from the network and validate it
        """
        if transaction.validate_signature(self.public_keys[transaction.emitter]):
            self.transaction_list.append(transaction)
            self.queue_to_node.put(transaction)

    def validate_block(self, block: Block):
        """
        This function will accept a block from the network and validate it
        """
        block.validate_signature(self.public_keys[block.header.validator_sign])
        if block not in self.node.blockchain: #Test this, not in uses __eq__ method
            self.node.blockchain.append(block)
            self.queue_to_node.put(block)