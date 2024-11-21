from subprocess import run
class Container:
    def __init__(self, name: str, real_port: int, VM_port: int, ip: str, network: str, image_name: str):
        self.name = name
        self.ip = ip
        self.real_port = real_port
        self.VM_port = VM_port
        self.network = network
        self.image_name = image_name
    
    def run_container(self, dettached = True):
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
            print(f"Container {self.name} with IP {self.ip} with ports {self.real_port}:{self.VM_port} lauched succesfully at network {self.network}")
        else:
            raise Exception(f"ERROR LAUNCING CONTAINER {self.name} with IP {self.ip} with ports {self.real_port}:{self.VM_port} at network {self.network}")
    
    
    def stop_container(self):
        command = [
            "docker", "stop",
            self.name
        ]
        command_output = run(command)
        if command_output.returncode == 0:
            print(f"Container {self.name} stopped succesfuly")
        else:
            raise Exception(f"Error stopping container {self.name}")
    
    def remove_container(self):
        command = [
            "docker", "rm",
            self.name
        ]
        command_output = run(command)
        if command_output.returncode == 0:
            print(f"Container {self.name} was removed successfuly")
        else:
            raise Exception(f"Error removing container {self.name}")
        
    def copy(self, file, directory):
        command = ["docker", "cp",
                    file, f"{self.name}:{directory}"]
        run(command)
    
    def create(self):
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
            print(f"Container {self.name} was created successfuly")
        else:
            raise Exception(f"Error creating container {self.name}")