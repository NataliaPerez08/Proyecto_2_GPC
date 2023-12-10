import socket
import sys
# Crea un socket TCP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Crear socket de cliente")

# El cliente recibirá como parámetros desde la línea de comandos la dirección IP del servidor y el puerto al cual se conectará.
if len(sys.argv) == 3:
    host = sys.argv[1]
    puerto = int(sys.argv[2])
    sock.connect((host, puerto))
else:
    print("Error: Debe ingresar la dirección IP del servidor y el puerto al cual se conectará")
    exit()
# Conecta el socket a la dirección localhost y el puerto 9999
#sock.connect(("localhost", 9999))

print("Conectando al servidor...")
print("Cliente, ¿Cual es su nombre?")
cliente_nombre = input()
# Enviarle el nombre del cliente al servidor
print("Cliente: Enviando mensaje al servidor con codigo 0: Nombre del cliente")
sock.send(int.to_bytes(0, length=1, byteorder='big'))

# Envia un mensaje al servidor
print("Cliente, ¿Desea capturar un pokemon?")
respuesta = int(input())
if respuesta == 1:
    print("Cliente: Enviando mensaje al servidor con codigo 10.")
    codigo_byte = int.to_bytes(10, length=1, byteorder='big')
    msg_byte = codigo_byte
    sock.send(msg_byte)
elif respuesta == 2:
    print("Cliente: Enviando mensaje al servidor con codigo 32")
    codigo_byte = int.to_bytes(32, length=1, byteorder='big')
    sock.send(codigo_byte)
else:
    print("Cliente: Respuesta inválida enviando mensaje al servidor con codigo 42")
    #"codigo":42,"msg":"Respuesta inválida"
    codigo_byte = int.to_bytes(42, length=1, byteorder='big')
    sock.send(codigo_byte)

sock.settimeout(10)
try:
    while True:
        # Recibe una respuesta del servidor
        data = sock.recv(1024)
        if not data:
            break

        codigo = data[0]
        if codigo == 20:
            print("Cliente: Recibí codigo 20")
            id_pokemon = str(data[1])

            print("Cliente, ¿Desea capturar el pokemon "+id_pokemon+"?: 1. Sí 2. No")
            respuesta = int(input())
            if respuesta == 1:
                print("Cliente: Enviando mensaje al servidor con codigo 30: Sí")
                codigo_byte = int.to_bytes(30, length=1, byteorder='big')
                sock.send(codigo_byte)
            elif respuesta == 2:
                print("Cliente: Enviando mensaje al servidor con codigo 31: No")
                codigo_byte = int.to_bytes(31, length=1, byteorder='big')
                sock.send(codigo_byte)


        if codigo == 21:
            print("Cliente: Recibí codigo 21")
            intentos = data[2]
            print("Cliente: Recibí ",intentos," intentos")

            print("Cliente, ¿Desea reintentar capturar el pokemon ",data[1],": 1. Sí 2. No")
            respuesta = int(input())
            if respuesta == 1:
                print("Cliente: Enviando mensaje al servidor con codigo 30: Sí")
                codigo_byte = int.to_bytes(30, length=1, byteorder='big')
                sock.send(codigo_byte)
            elif respuesta == 2:
                print("Cliente: Enviando mensaje al servidor con codigo 31: No")
                codigo_byte = int.to_bytes(31, length=1, byteorder='big')
                sock.send(codigo_byte)

        if codigo == 22:
            print("Cliente: Recibí codigo 22")
            id_pokemon = data[1]
            image_size = data[2:6]
            image = data[6:]
            print("Cliente: Recibí la imagen del pokemon con id= ",id_pokemon)
            int_image_size = int.from_bytes(image_size, byteorder='big')
            print("Tamaño de imagen: ",int_image_size)
            print("¿Desea guardar la imagen? 1. Sí 2. No")
            respuesta = int(input())
            if respuesta == 1:
                nombre_archivo = "pokemon"+str(id_pokemon)+".png"
                archivo = open(nombre_archivo, "wb")
                archivo.write(image)
                archivo.close()
                print("Cliente: Imagen guardada")
            elif respuesta == 2:
                print("Cliente: Imagen no guardada")
        
            print("Cliente, ¿Desea capturar otro pokemon? 1. Sí 2. No 3. Consultar pokemones capturados")
            respuesta = int(input())
            if respuesta == 1:
                print("Cliente: Enviando mensaje al servidor con codigo 10: Solicitar al servidor un pokemon")
                codigo_byte = int.to_bytes(10, length=1, byteorder='big')
                sock.send(codigo_byte)
            elif respuesta == 2:
                print("Cliente: Enviando mensaje al servidor con codigo 32: Terminando sesión")
                codigo_byte = int.to_bytes(32, length=1, byteorder='big')
                sock.send(codigo_byte)

            elif respuesta == 3:
                print("Cliente: Enviando mensaje al servidor con codigo 24. Solicitar al servidor la lista de pokemones capturados")
                #{'codigo':24,'msg':'Solicita pokemones capturados'}
                codigo_byte = int.to_bytes(24, length=1, byteorder='big')
                sock.send(codigo_byte)

        if codigo == 23:
            print("Cliente: Recibí codigo 23. Intentos de captura agotados")
            print("Cliente: Enviando mensaje al servidor con codigo 32: Terminando sesión")
            sock.send(int.to_bytes(32, length=1, byteorder='big'))

        if codigo == 25:
            print("Cliente: Recibí codigo 25")
            longitud = len(data)
            lista_pokemones = data[1:longitud]
            # Decodifica la lista de pokemones
            lista_pokemones = lista_pokemones.decode()
            print(lista_pokemones)
            #print("Pokemones capturados", lista_pokemones)
            print("Cliente, ¿Desea capturar otro pokemon? 1. Sí  2. No")
            respuesta = int(input())
            if respuesta == 1:
                print("Cliente: Enviando mensaje al servidor con codigo 10: Solicitar al servidor un pokemon")
                codigo_byte = int.to_bytes(10, length=1, byteorder='big')
                sock.send(codigo_byte)
            elif respuesta == 2:
                print("Cliente: Enviando mensaje al servidor con codigo 32: Terminando sesión")
                codigo_byte = int.to_bytes(32, length=1, byteorder='big')
                sock.send(codigo_byte)

        if codigo == 32:
            print("Cliente: Recibí codigo 32. Terminando sesión")
            break
        if codigo == 41:
            print("Cliente: Recibí codigo 41. Ocurrió un error en el servidor. Terminando sesión")
            break
        if codigo == 40:
            print("Cliente: Recibí codigo 40. Timeout: El servidor terminó la conexión.")
            break

        if codigo == 42:
            print("Cliente: Recibí codigo 42. Respuesta inválida del cliente.")
            break
        if codigo == 43:
            print("Cliente: Recibí codigo 43. Error: El usuario no existe. Terminando sesión.")
            break

except socket.timeout:
    print("Cliente: Timeout. Cerrando conexión con el servidor")
    sock.send(int.to_bytes(40, length=1, byteorder='big'))
    sock.close()

# Cierra el socket
sock.close()