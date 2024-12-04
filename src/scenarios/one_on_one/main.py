from comms.connection_handler import Connection_handler
import queue
import time
if __name__ == "__main__":
    data_queue = queue.Queue()
    handler = Connection_handler(5500, data_queue)
    handler.start()
    handler.data_queue.get()
    handler.broadcast("Welcome aboard capitain, all systems online")
    handler.data_queue.get()
    with open("mi_archivo.txt", "a") as archivo:
                    archivo.write("Sending last msg\n")  # Escribir una línea
    handler.broadcast("Hull integrity compromised.")