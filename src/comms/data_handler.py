"""
This class is in charge of accepting and refusing data transfers, it will have to check weather the sender is allowed to send data to the receiver, the transaction validation is done in transactions.
"""
import multiprocessing
from blockchain.transactionFactory import TransactionFactory
import json
from blockchain.structure.transaction import Transaction
from blockchain.structure.block import Block
 
class DataHandler:
    def __init__(self, queue_from_node: multiprocessing.Queue, queue_to_node: multiprocessing.Queue, public_keys: dict, blockchain, transaction_list, transaction_list_lock):
        """
        Connection handler is in charge of telling the connection_handler whether to broadcast a transaction or a block again, therefore to know whether my transaction has 
        been accepted by the network, I will have to receive my transaction again from the network.

        It is also in charge of validating data from the network and building the blockchain
        """
        self.queue_from_node = queue_from_node
        self.queue_to_node = queue_to_node
        self.public_keys = public_keys #Key dictionary with validator: public key
        self.transaction_list = transaction_list #This list will contain all the transactions that have been validated and received throught the network, it is shared with the Node
        self.blockchain = blockchain
        self.transaction_list_lock = transaction_list_lock #Lock to synchronize access to the transaction list, this is shared with the Node

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
                with open("logs.txt", "a") as logs_file:
                    logs_file.write(json.dumps(json_data, indent=4) + "\n")
            except json.JSONDecodeError:
                print(f"Data received was not in JSON format: {received_data}")
                with open("logs.txt", "a") as logs_file:
                    logs_file.write("The previous info was not in JSON format" + "\n")
                continue
            if "header" in json_data.keys() and "transactions" in json_data.keys():
                #if it contains a header field and a transactions field, it means it's a block
                with open("logs.txt", "a") as logs_file:
                    logs_file.write("Block was received\n")
                block = TransactionFactory.create_block(json_data)
                if block is None: 
                    print("Block was discaraded")
                    #If block could not be recovered, or was discarded, continue
                    continue
                elif block in self.blockchain:
                    #If block was already received, continue
                    print("Block was already received")
                    continue

                with open("logs.txt", "a") as logs_file:
                    logs_file.write("Validating block...\n")
                #If block is not in the blockchain, validate it, and if it's valid, add it to the blockchain
                is_valid_block = block.validate(self.public_keys, self.blockchain)
                if is_valid_block:
                    self.blockchain.append(block)
                    self.queue_to_node.put(block.serialize())
                    print(f"Block: \n {str(block.header)} \n was added to the blockchain")
                else:
                    with open("logs.txt", "a") as logs_file:
                        logs_file.write("Block was not valid\n") 
                    print("Block was discarded...")
            else:
                transaction = TransactionFactory.create_transaction(json_data)
                
                with open("logs.txt", "a") as archivo:
                    archivo.write("Data was a transaction\n") 
                if transaction is None:
                    print("Transaction was discaraded")
                    #If transaction could not be recovered, or was discarded, continue
                    continue
                elif transaction in self.transaction_list:
                    print("Transaction was already received")
                    #If transaction was already received, continue
                    continue
                    
                try:
                    
                    is_valid = transaction.validate(self.public_keys[transaction.emitter], self.blockchain)
                    with open("logs.txt", "a") as archivo:
                        archivo.write(f"is transaction valid? {is_valid}\n") 
                except KeyError:
                    print(f"Transaction {transaction.transaction_hash} was not valid, emitter {transaction.emitter} not found")
                    is_valid = False
                if is_valid:
                    #If the transaction is valid, add it to the transaction list and the queue to node
                    print(f"Accepted transaction {transaction}")
                    with self.transaction_list_lock:
                        #We use a lock to synchronize access to the transaction list
                        self.transaction_list.append(transaction)
                    self.queue_to_node.put(transaction.serialize())
                else:
                    print(f"Transaction {transaction} was not valid")