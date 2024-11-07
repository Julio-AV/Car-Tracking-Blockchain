from subprocess import run


def run_container(name: str, real_port: int, VM_port: int, ip: str, network: str, image_name: str):
    command = [
    "docker", "run",
    "--name", name,         # Container name
    "-p", f"{real_port}:{VM_port}",         # Port mapping
    "--ip", ip,     # IP
    "--network", network,  # Docker nework
    image_name          # Container image
    ]
    run(command)

name = "server"
real_port = 5000
VM_port = 5000
ip = "192.168.1.99"
network = "blockchain_network"
image_name = "imagen_juju"
run_container(name, real_port, VM_port, ip, network, image_name)