import socket
import queue
from comms.connection_handler import Connection_handler
import time
import utils.global_data_utils as global_data_utils
if __name__ == "__main__":
    machine_IP = "192.168.3.2"
    machine_port = 5500
    data_queue = queue.Queue()
    handler = Connection_handler(5500, data_queue)
    IPs_path = "IPs.csv"
    IPs = global_data_utils.read_list_from_csv(IPs_path)
    handler.open_multiple_connections(IPs)
    time.sleep(2)
    handler.send(machine_IP, "Soldiers! Do you hear me?")
    print("Data sent")
    handler.listen_once(machine_IP)
    handler.send(machine_IP, "Positions, now!")
    print("Second data sent")
    handler.listen_once(machine_IP)
    for IP in handler.open_connections.keys():
        handler.safe_close(IP)