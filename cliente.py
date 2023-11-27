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
msg23 = {"codigo":23,"msg":"Intentos de captura agotados"}
msg30 = {"codigo":30,"msg":"Sí"}
msg31 = {"codigo":31,"msg":"No"}
msg32 = {"codigo":32,"msg":"Terminando sesión"}

# Envia un mensaje al servidor
print("Cliente, ¿Desea capturar un pokemon?")
respuesta = input()
if respuesta == "Sí":
    print("Cliente: Enviando mensaje al servidor con codigo 10")
    sock.send(str(msg10).encode())
else:
    print("Cliente: Enviando mensaje al servidor con codigo 32")
    sock.send(str(msg32).encode())

while True:
    # Recibe una respuesta del servidor
    data = sock.recv(1024)
    if not data:
        break

    # Imprime la respuesta del servidor
    respuesta_servidor = eval(data.decode())
    codigo = respuesta_servidor['codigo']

    if codigo == 20:
        print("Cliente: Recibí codigo 20")
        print("Cliente: Recibí", respuesta_servidor['msg']," con pokemon", respuesta_servidor['pokemon'])

        print("Cliente, ¿Desea capturar el pokemon?"+respuesta_servidor['pokemon'])
        respuesta = input()
        if respuesta == "Sí":
            print("Cliente: Enviando mensaje al servidor con codigo 30: Sí")
            sock.send(str(msg30).encode())
        else:
            print("Cliente: Enviando mensaje al servidor con codigo 31: No")
            sock.send(str(msg31).encode())
        

    if codigo == 21:
        print("Cliente: Recibí codigo 21")
        print("Cliente: Recibí", respuesta_servidor['msg']," con", respuesta_servidor['intentos'],"intentos")
        print("Cliente: Enviando mensaje al servidor con codigo 30: Sí")
        msg30={'codigo':30,'msg':'Sí'}
        sock.send(str(msg30).encode())

    if codigo == 22:
        print("Cliente: Recibí codigo 22")
        print("Cliente: Recibí", respuesta_servidor['msg']," con pokemon", respuesta_servidor['pokemon'])
        print("Cliente, ¿Desea capturar otro pokemon?")
        respuesta = input()
        if respuesta == "Sí":
            print("Cliente: Enviando mensaje al servidor con codigo 10: Solicitar al servidor un pokemon")
            sock.send(str(msg10).encode())
        else:
            print("Cliente: Enviando mensaje al servidor con codigo 32: Terminando sesión")
            sock.send(str(msg32).encode())



    if codigo == 23:
        print("Cliente: Recibí codigo 23")
        print("Cliente: Recibí", respuesta_servidor['msg'])


    if codigo == 32:
        print("Cliente: Recibí codigo 32")
        break


# Cierra el socket
sock.close()