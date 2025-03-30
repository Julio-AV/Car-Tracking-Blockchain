"""
On this test file two containers will be deployed: One will be autonomous and the other one will be controled by you
"""
import os
import sys
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # 'src' is two levels above
print(f"Path added to sys.path: {src_dir}")
sys.path.insert(0, src_dir) #We need this lines to be able to use docker package
from docker import Container
from docker import create_network

#------------------------------------------------
#   Create keys and node information
#------------------------------------------------
from utils.key_handler import generate_and_store_keys, clear_key_files
from utils.key_handler import save_node_name, clear_node_files
node_names = ["autonomous_node", "manager_node"]
generate_and_store_keys(node_names)



DEPENDENCIES = ["comms", "utils", "blockchain"]
CONTAINER_INFO = ["data/node_info.json", "data/public_keys.json", "data/private_keys.json"]
DATA_PATH = "/app/data/"
container_main_path = "/app/"
#Autonomous container
# tc_name = "one_on_one_auto"
# tc_ip = "192.168.3.2"
# tc_real_port = 5500
# tc_VM_port = 5500
NETWORK = "test_network"
# tc_image = "node_image"
# main_path = "scenarios/one_on_one/main.py"
# create_network(tc_ip, NETWORK)
# test_container = Container(tc_name,tc_real_port, tc_VM_port, tc_ip, NETWORK, tc_image)
# test_container.create()
# test_container.copy(main_path, container_main_path)

# for dependency in DEPENDENCIES:
#     test_container.copy(dependency, container_main_path)
# for info in CONTAINER_INFO:
#     test_container.copy(info, DATA_PATH)

# #Copy the node name to it's container
# AUTONOMOUS_NODE_NAME = "autonomous_node"
# save_node_name(AUTONOMOUS_NODE_NAME, "data/node_info.json")
# test_container.copy("data/node_info.json", DATA_PATH)

#test_container.wake(dettached=False)



#Your container (manager)
m_name = "manager"
m_ip = "192.168.3.3"
m_real_port = 5501
m_VM_port = 5500
m_image = "manager_image"

manager_main_script = "scenarios/one_on_one/manager_main.py"
manager_node_implementation =  "scenarios/one_on_one/manager_node.py"
m_container = Container(m_name,m_real_port, m_VM_port, m_ip, NETWORK, m_image)
m_container.create()
m_container.copy(manager_main_script, container_main_path)
for dependency in DEPENDENCIES:
    m_container.copy(dependency, container_main_path)
for info in CONTAINER_INFO:
    m_container.copy(info, DATA_PATH)
#Copy the manager node implementation to the container
m_container.copy(manager_node_implementation, container_main_path+"/comms")
MANAGER_NODE_NAME = "manager_node"
save_node_name(MANAGER_NODE_NAME, "data/node_info.json")
m_container.copy("data/node_info.json", DATA_PATH)
m_container.wake_and_control()

#Clean containers
input("Push enter to remove containers")
#test_container.remove_container()
clear_key_files()
clear_node_files()
m_container.remove_container()
