from comms.connection_handler import Connection_handler
if __name__ == "__main__":
    handler = Connection_handler(5500)
    client_address = handler.accept_connection()
    handler.send(client_address, "Welcome aboard capitain, all systems online")
    handler.listen(client_address)
    handler.broadcast("Hull integrity compromised.")