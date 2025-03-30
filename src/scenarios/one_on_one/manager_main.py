import os
from comms.manager_node import ManagerNode #This might seem like an error, but once it's copied to the docker container, it's in the right path
#from scenarios.one_on_one.manager_node import ManagerNode
if __name__ == "__main__":
    print(f"Data path: {os.system("ls data")}")
    node: ManagerNode = ManagerNode()
    node.connection_handler.open_connection("192.168.3.2", 5500) #Ip of the machine, fix it to a proper manner in the future
    node.start()