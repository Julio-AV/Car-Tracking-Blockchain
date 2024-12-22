import os
import sys
import time
src_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))  # 'src' is two levels above
print(f"Path added to sys.path: {src_dir}")
sys.path.insert(0, src_dir) #We need this lines to be able to use docker package
from docker import Container
from docker import create_network

DEPENDENCIES = "comms"
CONTAINER_MAIN_PATH = "/app/"
N_TC = 2    #Number of autonomous containers
TC_BASE_NAME = "one_to_n_auto_"

TC_IP = "192.168.4."
last_IP_digit = 3
current_tc_real_port = 5500 #All containers will be assigned to a different machine port, this one marks the starting port
TC_VM_PORT = 5500 

NETWORK = "one_to_n_network"
TC_IMAGE = "socket_image"
MAIN_PATH = "scenarios/one_to_n/main.py"

create_network(TC_IP + "0", NETWORK)

container_list = []

for i in range(N_TC):
    current_tc_name = TC_BASE_NAME + str(i)
    current_IP = TC_IP + str(last_IP_digit)
    test_container = Container(current_tc_name, current_tc_real_port, TC_VM_PORT, current_IP, NETWORK, TC_IMAGE)
    test_container.create()
    test_container.copy(MAIN_PATH, CONTAINER_MAIN_PATH)
    test_container.copy(DEPENDENCIES, CONTAINER_MAIN_PATH)
    test_container.wake(dettached=True)
    container_list.append(test_container)
    current_tc_real_port +=1
    last_IP_digit += 1


m_name = "manager"
m_ip = "192.168.4.2"
m_real_port = 5501
m_VM_port = 5500
m_image = "manager_image"

m_test_script = "scenarios/one_to_n/manager_main.py"

m_container = Container(m_name,m_real_port, m_VM_port, m_ip, NETWORK, m_image)
m_container.create()
m_container.copy(MAIN_PATH, CONTAINER_MAIN_PATH)
m_container.copy(DEPENDENCIES, CONTAINER_MAIN_PATH)
m_container.copy(m_test_script, MAIN_PATH)
m_container.wake_and_control()

time.sleep(3)
for container in container_list:
    container.remove_container()

