from comms.connection_handler import Connection_handler
import queue
import time
import utils.global_data_utils as global_data_utils
if __name__ == "__main__":
    data_queue = queue.Queue()
    handler = Connection_handler(5500, data_queue)
    handler.start()
    IPs_path = "IPs.csv"
    IPs = global_data_utils.read_list_from_csv(IPs_path)
    handler.open_multiple_connections(IPs)
    data = handler.data_queue.get()    #First manager opening message
    handler.broadcast("Yes, sir!")
    for i in range(len(handler.open_connections.keys())):
        #Receive data from all connections
        handler.data_queue.get()
    handler.broadcast("On position, sir!")