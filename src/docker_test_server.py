import socket
import sys
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Vincular el socket a una dirección y puerto
server_address = ('0.0.0.0', int(sys.argv[1]))  # Puedes cambiar 'localhost' por la IP de tu servidor
server_socket.bind(server_address)

# Configurar el socket para escuchar conexiones
server_socket.listen(1)  # El argumento es el número de conexiones pendientes que el servidor puede tener

print("Esperando conexión...")

# Esperar y aceptar una conexión
connection, client_address = server_socket.accept()
print(f"Conexión establecida con {client_address}")
try:
    # Recibir datos en un bucle
    while True:
        data = connection.recv(1024)
        if data:
            print("Mensaje recibido:", data.decode())
            # Enviar respuesta al cliente
            connection.sendall("Mensaje recibido".encode())
        else:
            # No hay datos, cerrar la conexión
            print("Cerrando conexión")
            break
finally:
    # Limpiar
    connection.close()
    server_socket.close()