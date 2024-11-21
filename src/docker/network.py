import ipaddress
from subprocess import run
def is_valid_IP(ip):
    try:
        # Intentamos crear un objeto IP utilizando la dirección proporcionada
        ipaddress.ip_address(ip)
        return True  # Si no lanza excepción, la IP es válida
    except ValueError:
        raise Exception(f"Introduced IP address {ip} is not valid")
    

def create_network(starting_ip, network_name, mask = 24):
    """
    Creates a docker network
    
    Args:
        starting_ip: first container's IP
        network_name: Name of the network
        mask: subnet mask
    """
    is_valid_IP(starting_ip)
    splitted_IP = starting_ip.split(".")
    splitted_IP[-1] = "0"
    subnet = ".".join(splitted_IP)
    command = ["docker", "network" , "create",
                f"--subnet={subnet}/{mask}" , network_name]
    command_output = run(command)
    if command_output.returncode == 0:
        print(f"A new network has been created at: {subnet} with name {network_name}")
    else:
        print(f"New network {network_name} couln't be created at {subnet}")     