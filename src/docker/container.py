from subprocess import run
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
class Container:
    def __init__(self, name: str, real_port: int, VM_port: int, ip: str, network: str, image_name: str):
        self.name = name
        self.ip = ip
        self.real_port = real_port
        self.VM_port = VM_port
        self.network = network
        self.image_name = image_name
        
    def run_container(self, dettached = True):
        """
        Creates and runs the container
        """
        if dettached:
            command = [
                "docker", "run", "-d",
                "--name", self.name,         # Container name
                "-p", f"{str(self.real_port)}:{str(self.VM_port)}",         # Port mapping
                "--ip", self.ip,     # IP
                "--network", self.network,  # Docker nework
                self.image_name          # Container image
                ]
        else: 
            command = [
                "docker", "run",
                "--name", self.name,         # Container name
                "-p", f"{str(self.real_port)}:{str(self.VM_port)}",         # Port mapping
                "--ip", self.ip,     # IP
                "--network", self.network,  # Docker nework
                self.image_name          # Container image
                ]

        
        
        #print(f"name: {type(name)} ports {type(real_port)}:{type(VM_port)}, ip: {type(ip)} network: {type(network)}, image: {type(image_name)}")
        command_output = run(command)
        if command_output.returncode == 0:
            logging.info(f"Container {self.name} with IP {self.ip} with ports {self.real_port}:{self.VM_port} lauched succesfully at network {self.network}")
        else:
            raise Exception(f"ERROR LAUNCING CONTAINER {self.name} with IP {self.ip} with ports {self.real_port}:{self.VM_port} at network {self.network}")
    
    
    def stop_container(self):
        """
        Stops the container
        """
        command = [
            "docker", "stop",
            self.name
        ]
        command_output = run(command)
        if command_output.returncode == 0:
            logging.info(f"Container {self.name} stopped succesfuly")
        else:
            #raise Exception(f"Error stopping container {self.name}")
            logging.error(f"Error stopping container {self.name}")
    
    def remove_container(self):
        """
        Removes the container
        """
        self.stop_container()
        command = [
            "docker", "rm",
            self.name
        ]
        command_output = run(command)
        if command_output.returncode == 0:
            logging.info(f"Container {self.name} was removed successfuly")
        else:
            logging.error(f"Error removing container {self.name}")
        
    def copy(self, local, docker_dir):
        """
        Copies a file or directory to the container
        """
        command = ["docker", "cp",
                    local, f"{self.name}:{docker_dir}"]
        run(command)
    
    def create(self):
        """
        Creates a docker container without running it
        """
        command = [
                "docker", "create",
                "--name", self.name,         # Container name
                "-p", f"{str(self.real_port)}:{str(self.VM_port)}",         # Port mapping
                "--ip", self.ip,     # IP
                "--network", self.network,  # Docker nework
                self.image_name          # Container image
                ]
        command_output = run(command)
        if command_output.returncode == 0:
            logging.info(f"Container {self.name} was created successfuly")
        else:
            raise Exception(f"Error creating container {self.name}")
        
    def wake(self, dettached = True):
        if dettached:
            command = ["docker", "start",
                   self.name]
        else:
            command = ["docker", "start", "-a",
                       self.name]
        
        command_output = run(command)
        if command_output.returncode == 0:
            logging.info(f"Container {self.name} was woken successfuly")
        else:
            raise Exception(f"Error waking container {self.name}")
        
    def control(self):
        command = ["docker", "exec", "-it", 
                   self.name, "bash"]
        command_output = run(command)
        ret_code = command_output.returncode
        if ret_code == 0:
            print(f"Container {self.name} was controled successfuly")
        elif ret_code == 127:
            logging.error(f"Error executing command in container {self.name}")
        else:
            raise Exception(f"Error controling container {self.name}")
        

    def wake_and_control(self):
        self.wake()
        self.control()
        
    
    def run_and_control(self):
        """UNTESTED"""
        command = [
                "docker", "run", "-it",
                "--name", self.name,         # Container name
                "-p", f"{str(self.real_port)}:{str(self.VM_port)}",         # Port mapping
                "--ip", self.ip,     # IP
                "--network", self.network,  # Docker nework
                self.image_name          # Container image
                ]
        command_output = run(command)
        if command_output.returncode == 0:
            logging.info(f"Container {self.name} with IP {self.ip} with ports {self.real_port}:{self.VM_port} lauched succesfully at network {self.network}")
        else:
            raise Exception(f"ERROR LAUNCING CONTAINER {self.name} with IP {self.ip} with ports {self.real_port}:{self.VM_port} at network {self.network}")