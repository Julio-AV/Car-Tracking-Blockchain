import socket
from comms.connection_handler import Connection_handler
machine_IP = "192.168.3.2"
machine_port = 5500
handler = Connection_handler(5500)
handler.open_connection(machine_IP, machine_port)
rec = handler.listen(machine_IP)
print(rec)
handler.send(machine_IP, "Let's dive into the unknown!")
rec = handler.listen(machine_IP)
print(rec)