
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
N_GOV = 1 #Number of governmental institutions
N_INSURANCE = 1 #Number of insurance companies
N_VIS = 1 #Number of vehicle inspection stations
TC_BASE_IP = "192.168.5." #Base IP for the autonomous containers
IP_OFFSET = 3 #Offset for the IPs of the autonomous containers
TC_VM_PORT = 5500 
IPs = [] #List to store the IPs of the autonomous containers
node_names = [] #List to store the node names of the autonomous containers
container_i = 0 #Counter for the autonomous containers
#---------------------------------
#Create governmental institutions

for i in range(N_GOV):
    IPs.append(TC_BASE_IP + str( container_i + IP_OFFSET)) #Generate IPs for the governmental institutions
    container_i += 1
    node_names.append("gov_" + str(i)) #Generate node names for the governmental institutions

for i in range(N_INSURANCE):
    IPs.append(TC_BASE_IP + str( container_i + IP_OFFSET)) #Generate IPs for the insurance companies
    container_i += 1
    node_names.append("insurance_" + str(i)) #Generate node names for the insurance companies

for i in range(N_VIS):
    IPs.append(TC_BASE_IP + str( container_i + IP_OFFSET)) #Generate IPs for the vehicle inspection stations
    container_i += 1
    node_names.append("vis_" + str(i)) #Generate node names for the vehicle inspection stations

#---------------------------------
#   Manager container
#---------------------------------
M_NAME = "manager"
M_IP = "192.168.5.2"
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
DEPENDENCIES = ["comms", "utils", "blockchain", "data"]
CONTAINER_MAIN_PATH = "/app/"



DOCKER_NETWORK_NAME = "realistic_network"

MAIN_PATH = "scenarios/one_to_n/main.py"
create_network(TC_BASE_IP + "0", DOCKER_NETWORK_NAME) #Create the network for the containers

TC_IMAGE = "node_image" #This dockerfile is in the base path, so build the image before using it

container_list = [] #List to store the containers

for i in range(len(IPs)-1):
    current_container_name = node_names[i]
    current_container_ip = IPs[i]
    current_node_info = {"node_name": current_container_name, "IP": current_container_ip}
    save_node_info(current_node_info)  # Save node info to file
    current_tc_real_port = 5500 + i + 1#All containers will be assigned to a different machine port : 5501, 5502, etc. +1 since manager's port is 5500
    container = Container(current_container_name, current_tc_real_port, TC_VM_PORT, current_container_ip, DOCKER_NETWORK_NAME, TC_IMAGE)
    container.create()
    #Get main path depending on the type of node it is: 
    if current_container_name.startswith("gov_"):
        main_path = "scenarios/realistic_scenario/roles/GovernmentalInstitution.py"
    elif current_container_name.startswith("insurance_"):
        main_path = "scenarios/realistic_scenario/roles/InsuranceCompany.py"
    elif current_container_name.startswith("vis_"):
        main_path = "scenarios/realistic_scenario/roles/VIS.py"
    else:
        raise ValueError(f"Unknown node type for container: {current_container_name}")
    container.copy(main_path, CONTAINER_MAIN_PATH + "main.py")  # Copy the main file to the container
    # Copy dependencies
    for dependency in DEPENDENCIES:
        container.copy(dependency, CONTAINER_MAIN_PATH)
    container.wake()
    container_list.append(container)  # Add the container to the list
#---------------------------------
#   Manager container
#---------------------------------
MANAGER_SCRIPT_PATH = "scenarios/realistic_scenario/roles/manager.py"
m_container = Container(M_NAME, m_real_port, M_VM_PORT, M_IP, DOCKER_NETWORK_NAME, M_IMAGE)
m_container.create()
m_container.copy(MANAGER_SCRIPT_PATH, CONTAINER_MAIN_PATH)  # Copy the manager script to the container
manager_node_info = {"node_name": M_NAME, "IP": M_IP}
save_node_info(manager_node_info) #Save the node info for the manager container
for dependency in DEPENDENCIES:
    m_container.copy(dependency, CONTAINER_MAIN_PATH)  # Copy dependencies to the manager container
m_container.wake_and_control()  # Wake the manager container and control it


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