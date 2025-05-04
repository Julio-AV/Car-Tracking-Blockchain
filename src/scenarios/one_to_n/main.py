from comms.node import Node
import os
if __name__ == "__main__":
    print(f"Data path: {os.listdir('data')}")
    node = Node()
    node.start()