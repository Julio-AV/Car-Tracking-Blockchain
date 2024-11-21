"""
On this test file two containers will be deployed: One will be autonomous and the other one will be controled by you
"""

from docker import Container
from docker import create_network
if __name__ == "__main__":
    tc_name = "one_on_one_auto"
    tc_ip = "192.168.2.2"
    tc_real_port = 5500
    tc_VM_port = 5500
    tc_network = "test_network"
    tc_image = "imagen_socket"
    create_network(tc_ip, tc_network)
    test_container = Container(tc_name,tc_real_port, tc_VM_port, tc_ip, tc_network, tc_image)
    test_container.create()
    test_container.copy()
    test_container.run_container()

    test_container.remove_container()