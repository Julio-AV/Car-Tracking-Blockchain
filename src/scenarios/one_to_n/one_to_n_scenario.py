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
#------------------------------------------------
#   Create keys and node information
#------------------------------------------------
from utils.key_handler import generate_and_store_keys, clear_key_files, save_node_info, clear_node_files
from utils.IP_file_handler import generate_connected_network, write_connections_to_file, delete_connections_file
#------------------------------------------------
        #Autonomous containers
#------------------------------------------------
N_TC = 2    #Number of autonomous containers
TC_BASE_IP = "192.168.4." #Base IP for the autonomous containers
IP_OFFSET = 3 #Offset for the IPs of the autonomous containers
TC_BASE_NAME = "one_to_n_auto_" #Base name for the autonomous containers
TC_VM_PORT = 5500 

IPs = [TC_BASE_IP + str(i + IP_OFFSET) for i in range(N_TC)] #Generate IPs for the containers
node_names = [TC_BASE_NAME + str(i) for i in range(N_TC)] #Generate node names for the containers

#---------------------------------
#   Manager container
#---------------------------------
M_NAME = "manager_one_to_n"
M_IP = "192.168.4.2"
m_real_port = 5500
M_VM_PORT = 5500
M_IMAGE = "manager_image"   #This dockerfile is in one_on_one path, so build the image before using it

IPs.append(M_IP) #Add the manager IP to the list of IPs
node_names.append(M_NAME) #Add the manager name to the list of node names

#Generate keys for the containers
generate_and_store_keys(node_names) #Generate the keys for the containers

#Generate connections   
generatedd_network = generate_connected_network(IPs) #Generate the connections for the containers
write_connections_to_file(generatedd_network) #Store connections








#------------------------------------------------
        #Start container network
#------------------------------------------------

#Global info
DEPENDENCIES = ["comms", "utils", "blockchain", "data"]
CONTAINER_MAIN_PATH = "/app/"



DOCKER_NETWORK_NAME = "one_to_n_network"

MAIN_PATH = "scenarios/one_to_n/main.py"

create_network(TC_BASE_IP + "0", DOCKER_NETWORK_NAME) #Create the network for the containers

#CREATE AUTONOMOUS CONTAINERS

TC_IMAGE = "node_image" #This dockerfile is in the base path, so build the image before using it
container_list = [] #List to store the containers

for i in range(N_TC):
    current_tc_name = node_names[i]
    current_IP = IPs[i]
    current_node_info = {"node_name": current_tc_name, "IP": current_IP}
    save_node_info(current_node_info) #Save the node info for the container
    current_tc_real_port = 5500 + i + 1 #All containers will be assigned to a different machine port : 5501, 5502, etc. +1 since manager's port is 5500
    test_container = Container(current_tc_name, current_tc_real_port, TC_VM_PORT, current_IP, DOCKER_NETWORK_NAME, TC_IMAGE)
    test_container.create()
    test_container.copy(MAIN_PATH, CONTAINER_MAIN_PATH)  #Copy file that will be executed once the container wakes
    for dependency in DEPENDENCIES:
        #Copy the dependencies
        test_container.copy(DEPENDENCIES[i], CONTAINER_MAIN_PATH)  
    test_container.wake(dettached=True)
    container_list.append(test_container)


#CREATE MANAGER CONTAINER

M_TEST_SCRIPT_PATH = "scenarios/one_to_n/manager_main.py"

m_container = Container(M_NAME, m_real_port, M_VM_PORT, M_IP, DOCKER_NETWORK_NAME, M_IMAGE)
m_container.create()
m_container.copy(M_TEST_SCRIPT_PATH, CONTAINER_MAIN_PATH) #Copy manager script that YOU will manually execute inside the container
for dependency in DEPENDENCIES:
    #Copy the dependencies
    m_container.copy(dependency, CONTAINER_MAIN_PATH)
m_container.wake_and_control()


#Cleanup
input("\nPress enter to remove containers:")
#Clear containers
for container in container_list:
    container.remove_container() 
m_container.remove_container()
#Clear data files
clear_key_files()
clear_node_files()
delete_connections_file()

