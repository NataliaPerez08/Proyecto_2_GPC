import socket

# Crea un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Crear socket de cliente")

# Conecta el socket a la dirección localhost y el puerto 8080
print("Conectando al servidor")
sock.connect(("localhost", 9999))

# Tipos de mensajes: {codigo:x, mensaje:y}
msg10 = {"codigo":10,"msg":"Solicitar al servidor un pokemon"}

msg20 = {"codigo":20,"msg":"¿Capturar pokemon?","pokemon":'x-pokemon'}
msg21 = {"codigo":21,"msg":"¿Intentar captura de nuevo?","intentos":0}
msg22 = {"codigo":22,"msg":"Envia pokemon capturado","pokemon":'x-pokemon'}

msg23 = {"codigo":23,"msg":"Intentos de captura agotados"}

msg30 = {"codigo":30,"msg":"Sí"}
msg31 = {"codigo":31,"msg":"No"}

msg = {"codigo":0,"msg":"Mensaje de prueba"}


print(msg21)
# Envia un mensaje al servidor
i = 0
for i in range(3):
    print("Enviando mensaje al servidor")
    sock.sendall(str(msg10).encode())

    # Recibe una respuesta del servidor
    data = sock.recv(1024)

    # Imprime la respuesta del servidor
    print(data.decode())

# Cierra el socket
sock.close()