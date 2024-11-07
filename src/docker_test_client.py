import socket
import sys
# Crear un socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar al servidor en 'localhost' y puerto 65432
server_address = ('192.168.1.99', 5000)
client_socket.connect(server_address)

try:
    # Enviar un mensaje al servidor
    message = "Hola, servidor!"
    print("Enviando:", message)
    client_socket.sendall(message.encode())

    # Esperar respuesta del servidor
    data = client_socket.recv(1024)
    print("Respuesta del servidor:", data.decode())

finally:
    # Limpiar
    print("Cerrando conexión")
    client_socket.close()