"""
Script designed to generate a 1 to n fully connected network where the manager container will be controlled by the user
"""

import os
import sys
import time
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # 'src' is two levels above
print(f"Path added to sys.path: {src_dir}")
sys.path.insert(0, src_dir) #We need this lines to be able to use docker package
from docker import Container
from docker import create_network
import utils.IP_file_handler as IP_file_handler
DEPENDENCIES_PATH = "comms"
UTILS_PATH = "utils"
CONTAINER_MAIN_PATH = "/app/"
N_TC = 2    #Number of autonomous containers
TC_BASE_NAME = "one_to_n_auto_"

TC_IP = "192.168.4."
IP_OFFSET = 3
current_tc_real_port = 5500 #All containers will be assigned to a different machine port, this one marks the starting port
TC_VM_PORT = 5500 

NETWORK = "one_to_n_network"
TC_IMAGE = "socket_image"
MAIN_PATH = "scenarios/one_to_n/main.py"
IP_FILE = "IPs.csv"
IPs = [TC_IP + str(i + IP_OFFSET) for i in range(N_TC)]

IP_file_handler.write_list_to_csv(IP_FILE, IPs)

create_network(TC_IP + "0", NETWORK)

container_list = []

for i in range(N_TC):
    current_tc_name = TC_BASE_NAME + str(i)
    current_IP = IPs[i]
    test_container = Container(current_tc_name, current_tc_real_port, TC_VM_PORT, current_IP, NETWORK, TC_IMAGE)
    test_container.create()
    test_container.copy(MAIN_PATH, CONTAINER_MAIN_PATH)  #Copy file that will be executed once the container wakes
    test_container.copy(DEPENDENCIES_PATH, CONTAINER_MAIN_PATH)  #Copy the dependencies
    test_container.copy(IP_FILE, CONTAINER_MAIN_PATH)  #Copy the files with the IPs that the container will connect to
    test_container.copy(UTILS_PATH, CONTAINER_MAIN_PATH)  #Copy the utils
    test_container.wake(dettached=True)
    container_list.append(test_container)
    current_tc_real_port +=1

M_NAME = "manager_one_to_n"
M_IP = "192.168.4.2"
m_real_port = current_tc_real_port
M_VM_PORT = 5500
M_IMAGE = "manager_image"   #This dockerfile is in one_on_one path, so build the image before using it

M_TEST_SCRIPT_PATH = "scenarios/one_to_n/manager_main.py"

m_container = Container(M_NAME, m_real_port, M_VM_PORT, M_IP, NETWORK, M_IMAGE)
m_container.create()
m_container.copy(MAIN_PATH, CONTAINER_MAIN_PATH)
m_container.copy(DEPENDENCIES_PATH, CONTAINER_MAIN_PATH)
m_container.copy(M_TEST_SCRIPT_PATH, CONTAINER_MAIN_PATH)
m_container.copy(IP_FILE, CONTAINER_MAIN_PATH)  #Copy the files with the IPs that the container will connect to
m_container.copy(UTILS_PATH, CONTAINER_MAIN_PATH)  #Copy the utils
m_container.wake_and_control()

#Cleanup
for container in container_list:
    container.remove_container()
m_container.remove_container()

IP_file_handler.delete_file(IP_FILE)

