from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
import json
import os

def generate_and_store_keys(node_names: list, public_file='public_keys.json', private_file='private_keys.json'):
    public_keys = {}
    private_keys = {}
    
    for key_name in node_names:
        # Obtain private key
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        # Obtain public key
        public_key = private_key.public_key()
        # Serialize keys
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode()
        
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ).decode()
        
        # Add to dictionaries
        public_keys[key_name] = public_pem
        private_keys[key_name] = private_pem
    
    # Store in JSON files
    with open(public_file, 'w') as pub_file:
        json.dump(public_keys, pub_file, indent=4)
    
    with open(private_file, 'w') as priv_file:
        json.dump(private_keys, priv_file, indent=4)
    
    print("Keys generated and stored successfully.")

def load_keys(key_name, public_file='public_keys.json', private_file='private_keys.json'):
    """
    Load al public keys in a dictionary and load node own private key
    """
    try:
        with open(public_file, 'r') as pub_file:
            public_keys_data = json.load(pub_file)
        with open(private_file, 'r') as priv_file:
            private_keys = json.load(priv_file)
        
        private_pem = private_keys.get(key_name)

        public_keys = {}
        for key_name, public_pem in public_keys_data.items():
            public_keys[key_name] = serialization.load_pem_public_key(public_pem.encode())

        if private_pem:
            private_key = serialization.load_pem_private_key(private_pem.encode(), password=None)
            return public_keys, private_key
        else:
            raise ValueError(f"Key {key_name} not found.")
    except FileNotFoundError:
        raise FileNotFoundError("Key file not found.")

def clear_key_files(public_file='public_keys.json', private_file='private_keys.json'):
    try:
        if os.path.exists(public_file):
            os.remove(public_file)
        if os.path.exists(private_file):
            os.remove(private_file)
        print("Key files cleared succerssfully.")
    except Exception as e:
        print(f"Error deleting key files: {e}")


def save_node_name(node_name, node_file='node_info.json'):
    """
    Write a node name to a file (file is a JSON with a single key "node_name")
    """
    with open(node_file, 'w') as file:
        json.dump({"node_name": node_name}, file, indent=4)
    print("Nombre del nodo guardado correctamente.")

def load_node_name(node_file='node_info.json'):
    """
    Load node name from a file (file is a JSON with a single key "node_name")
    """
    try:
        with open(node_file, 'r') as file:
            data = json.load(file)
            return data.get("node_name")
    except FileNotFoundError:
        raise FileNotFoundError("Archivo de información del nodo no encontrado.")

def clear_key_files(node_file='node_info.json'):
    try:
        if os.path.exists(node_file):
            os.remove(node_file)
    except Exception as e:
        print(f"Error deleting node file {node_file}: {e}")


if __name__ == '__main__':
    generate_and_store_keys(["usuario1", "usuario2"])
    public_keys, private_key = load_keys("usuario2")
    print(public_keys)
    print(type(private_key))
    clear_key_files()