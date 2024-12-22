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

dependencies = "comms"
container_main_path = "/app/"
#Autonomous container
tc_name = "one_on_one_auto"
tc_ip = "192.168.3.2"
tc_real_port = 5500
tc_VM_port = 5500
NETWORK = "test_network"
tc_image = "socket_image"
main_path = "scenarios/one_on_one/main.py"
create_network(tc_ip, NETWORK)
test_container = Container(tc_name,tc_real_port, tc_VM_port, tc_ip, NETWORK, tc_image)
test_container.create()
test_container.copy(main_path, container_main_path)
test_container.copy(dependencies, container_main_path)
test_container.wake(dettached=False)



#Your container (manager)
m_name = "manager"
m_ip = "192.168.3.3"
m_real_port = 5501
m_VM_port = 5500
m_image = "manager_image"

m_test_script = "scenarios/one_on_one/manager_main.py"

m_container = Container(m_name,m_real_port, m_VM_port, m_ip, NETWORK, m_image)
m_container.create()
m_container.copy(main_path, container_main_path)
m_container.copy(dependencies, container_main_path)
m_container.copy(m_test_script, container_main_path)
m_container.wake_and_control()

#Clean containers
test_container.remove_container()
#m_container.remove_container()
