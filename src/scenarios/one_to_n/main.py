from comms.connection_handler import ConnectionHandler
import queue
import time
import utils.IP_file_handler as IP_file_handler
if __name__ == "__main__":
    data_queue = queue.Queue()
    handler = ConnectionHandler(5500, data_queue)
    handler.start()
    IPs_path = "IPs.csv"
    IPs = IP_file_handler.read_list_from_csv(IPs_path)
    handler.open_multiple_connections(IPs)
    data = handler.data_queue.get()    #First manager opening message
    handler.broadcast("Yes, sir!")
    for i in range(len(handler.open_connections.keys())):
        #Receive data from all connections
        handler.data_queue.get()
    handler.broadcast("On position, sir!")