import socket
import random

import threading
from _thread import start_new_thread
print_lock = threading.Lock()

def threaded(conn, addr):
    msg20 = {"codigo":20,"msg":"¿Capturar pokemon?","pokemon":'x-pokemon'}
    msg21 = {"codigo":21,"msg":"¿Intentar captura de nuevo?","intentos":10}
    msg22 = {"codigo":22,"msg":"Envia pokemon capturado","pokemon":'x-pokemon'}
    msg23 = {"codigo":23,"msg":"Intentos de captura agotados"}
    msg30 = {"codigo":30,"msg":"Sí"}
    msg31 = {"codigo":31,"msg":"No"}
    msg32 = {"codigo":32,"msg":"Terminando sesión"}
    msg = {"codigo":0,"msg":"Mensaje de prueba"}
    while True:
        # Recibe un mensaje del cliente
        data = conn.recv(1024)
        if data:  
            msg_cliente = eval(data.decode())
            codigo = msg_cliente['codigo']

            if codigo == 10:
                print("Servidor: Recibí solicitud de pokemon")
                msg20['pokemon'] = 'pokemon1'
                #conn.sendall(str(msg20).encode())
                print("Servidor: Enviando pokemon al cliente",addr[0],':',addr[1])
                conn.send(str(msg20).encode())

            if codigo == 30:
                print("Servidor: Recibí respuesta afirmativa de captura de pokemon")
                capturado = random.randint(0,1)

                if capturado == 1:
                    print("Servidor: Pokemon capturado")
                    msg22 = {"codigo":22,"msg":"Pokemon capturado","pokemon":'x-pokemon'}
                    msg22['pokemon'] = 'pokemon1'
                    conn.send(str(msg22).encode())
                else:
                    print("Servidor: Pokemon no capturado")
                    intentos = msg21['intentos'] - 1
                    msg21 = {"codigo":21,"msg":"¿Intentar captura de nuevo?","intentos":intentos}
                    conn.send(str(msg21).encode())
                    intentos = intentos - 1
                    if intentos == 0:
                        print("Servidor: Intentos de captura agotados")
                        conn.send(str(msg23).encode())

            if codigo == 31:
                print("Servidor: Recibí respuesta negativa de captura de pokemon")
                print("Servidor: Enviando mensaje de terminar sesión")
                conn.send(str(msg32).encode())

            if codigo == 32:
                print("Servidor: Recibí solicitud de terminar sesión")
                conn.send(str(msg32).encode())
                #print_lock.release()
                break
        else:
            print_lock.release()
            break

def Main():
    host = ""
    port = 9999
    # Crea un socket TCP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Escucha conexiones en el puerto 9999
    sock.bind((host, port))
    print("El socket está enlazado al puerto", port)
    sock.listen(5)
    print("El socket está escuchando")
	
    while True:
        # Acepta una conexión
        conn, addr = sock.accept()
        # Lock adquirido por el cliente
        #print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        start_new_thread(threaded, (conn,addr))
        #sock.close()

if __name__ == '__main__':
	Main()
