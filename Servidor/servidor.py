import socket

# Crea un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Escucha conexiones en el puerto 8080
sock.bind(("localhost", 9999))
sock.listen(1)

# Acepta una conexión
conn, addr = sock.accept()

while True:
    # Recibe un mensaje del cliente
    data = conn.recv(1024)
    if not data:
        break
    # Imprime el mensaje del cliente
    print(data.decode())

    # Envía una respuesta al cliente
    conn.sendall("Hola, cliente!".encode())

# Cierra la conexión
conn.close()