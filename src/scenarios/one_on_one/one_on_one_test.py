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



tc_name = "one_on_one_auto"
tc_ip = "192.168.3.2"
tc_real_port = 5500
tc_VM_port = 5500
tc_network = "test_network"
tc_image = "imagen_socket"
main_path = "scenarios/one_on_one/main.py"
create_network(tc_ip, tc_network)
test_container = Container(tc_name,tc_real_port, tc_VM_port, tc_ip, tc_network, tc_image)
test_container.create()
test_container.copy(main_path, "/app/")
test_container.wake()
test_container.remove_container()