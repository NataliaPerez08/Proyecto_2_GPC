import socket

# Crea un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Crear socket de cliente")

print("Ingresar ip del servidor")
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
respuesta = int(input())
if respuesta == 1:
    print("Cliente: Enviando mensaje al servidor con codigo 10")
    codigo_byte = bytes([10])
    msg_byte = bytes(msg10['msg'].encode())
    sock.send(codigo_byte + msg_byte)
    #sock.send(str(msg10).encode())
elif respuesta == 2:
    print("Cliente: Enviando mensaje al servidor con codigo 32")
    sock.send(str(msg32).encode())
else:
    print("Cliente: Respuesta inválida enviando mensaje al servidor con codigo 42")
    msg42 = {"codigo":42,"msg":"Respuesta inválida"}
    sock.send(str(msg42).encode())

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

        print("Cliente, ¿Desea capturar el pokemon "+respuesta_servidor['pokemon']+"?: 1. Sí 2. No")
        respuesta = int(input())
        if respuesta == 1:
            print("Cliente: Enviando mensaje al servidor con codigo 30: Sí")
            sock.send(str(msg30).encode())
        elif respuesta == 2:
            print("Cliente: Enviando mensaje al servidor con codigo 31: No")
            sock.send(str(msg31).encode())


    if codigo == 21:
        print("Cliente: Recibí codigo 21")
        print("Cliente: Recibí", respuesta_servidor['msg']," con", respuesta_servidor['intentos'],"intentos")

        print("Cliente, ¿Desea reintentar capturar el pokemon?: 1. Sí 2. No")
        respuesta = int(input())
        if respuesta == 1:
            print("Cliente: Enviando mensaje al servidor con codigo 30: Sí")
            sock.send(str(msg30).encode())
        elif respuesta == 2:
            print("Cliente: Enviando mensaje al servidor con codigo 31: No")
            sock.send(str(msg31).encode())

    if codigo == 22:
        print("Cliente: Recibí codigo 22")
        print("Cliente: Recibí", respuesta_servidor['msg']," con pokemon", respuesta_servidor['pokemon'])
        print("Cliente, ¿Desea capturar otro pokemon? 1. Sí 2. No 3. Consultar pokemones capturados")
        respuesta = int(input())
        if respuesta == 1:
            print("Cliente: Enviando mensaje al servidor con codigo 10: Solicitar al servidor un pokemon")
            sock.send(str(msg10).encode())
        elif respuesta == 2:
            print("Cliente: Enviando mensaje al servidor con codigo 32: Terminando sesión")
            sock.send(str(msg32).encode())
        elif respuesta == 3:
            print("Cliente: Pokemones capturados", respuesta_servidor['pokemon'])
            msg24={'codigo':24,'msg':'Solicita pokemones capturados'}
            sock.send(str(msg24).encode())        
            print("Cliente: Enviando mensaje al servidor con codigo 24. Solicitar al servidor la lista de pokemones capturados")

    if codigo == 23:
        print("Cliente: Recibí codigo 23. Intentos de captura agotados")
        print("Cliente: Enviando mensaje al servidor con codigo 32: Terminando sesión")
        sock.send(str(msg32).encode())

    if codigo == 25:
        print("Cliente: Recibí codigo 25")
        print("Pokemones capturados", respuesta_servidor['pokemones'])
        print("Cliente, ¿Desea capturar otro pokemon? 1. Sí  2. No")
        respuesta = int(input())
        if respuesta == 1:
            print("Cliente: Enviando mensaje al servidor con codigo 10: Solicitar al servidor un pokemon")
            sock.send(str(msg10).encode())
        elif respuesta == 2:
            print("Cliente: Enviando mensaje al servidor con codigo 32: Terminando sesión")
            sock.send(str(msg32).encode())

    if codigo == 32:
        print("Cliente: Recibí codigo 32")
        print("Terminando sesión")
        break


# Cierra el socket
sock.close()