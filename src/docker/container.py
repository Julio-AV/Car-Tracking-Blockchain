class container:
    def __init__(self, name: str, real_port: int, VM_port: int, ip: str, network: str, image_name: str):
        self.name = name
        self.ip = ip
        self.real_port = real_port
        self.VM_port = VM_port
        self.network = network
        self.image_name = image_name
    
        