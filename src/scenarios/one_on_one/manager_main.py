import socket
import queue
from comms.connection_handler import ConnectionHandler
import time
machine_IP = "192.168.3.2"
machine_port = 5500
data_queue = queue.Queue()
handler = ConnectionHandler(5500, data_queue)
handler.open_connection(machine_IP, machine_port)
time.sleep(2)
handler.send(machine_IP, "Hello Cyclops")
print("Data sent")
handler.listen_once(machine_IP)
handler.send(machine_IP, "Let's dive into the unknown!")
print("Second data sent")
handler.listen_once(machine_IP)
handler.safe_close(machine_IP)