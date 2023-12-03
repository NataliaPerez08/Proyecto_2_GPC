import socket
import random
import conexionPokeAPi  as pokeapi
# Partially-mapped crossover (PMX)
# Order crossover (OX)
from _thread import start_new_thread
def threaded(conn, addr):
  
    pokemon_actual = ""
    lista_pokemones = []
    intentos = 5 # Valor inicial
    msg21 = {"codigo":21,"msg":"¿Intentar captura de nuevo?","intentos":intentos}
    while True:
        # Recibe un mensaje del cliente
        data = conn.recv(1024)
        if data: 
            try:
                msg_cliente = eval(data.decode())
                codigo = msg_cliente['codigo']
            except SyntaxError:
                print("Servidor: Recibí mensaje inválido del cliente",addr[0],':',addr[1])
                print(data.decode())

            if codigo == 10:
                print("Servidor: Recibí solicitud de pokemon")
                pokemon_actual = pokeapi.obtener_pokemon()['name']
                msg20 = {"codigo":20,"msg":"¿Capturar pokemon?","pokemon":pokemon_actual}
                print("Servidor: Enviando pokemon al cliente",addr[0],':',addr[1])
                conn.send(str(msg20).encode())

            if codigo == 30:
                print("Servidor: Recibí respuesta afirmativa de captura de pokemon del cliente",addr[0],':',addr[1])
                capturado = random.randint(0,10)

                if capturado == 1:
                    print("Servidor: Pokemon capturado del cliente",addr[0],':',addr[1])
                    msg22 = {"codigo":22,"msg":"Pokemon capturado","pokemon":pokemon_actual}
                    lista_pokemones.append(pokemon_actual)
                    conn.send(str(msg22).encode())
                else:
                    print("Servidor: Pokemon no capturado del cliente",addr[0],':',addr[1])
                    intentos = msg21['intentos'] - 1
                    if intentos == 0:
                        print("Servidor: Intentos de captura agotados")
                        msg23 = {"codigo":23,"msg":"Intentos de captura agotados"}
                        conn.send(str(msg23).encode())
                    else:
                        msg21 = {"codigo":21,"msg":"¿Intentar captura de nuevo?","intentos":intentos}
                        conn.send(str(msg21).encode())
                        intentos = intentos - 1
            if codigo == 24:
                print("Servidor: Recibí solicitud de pokemones capturados del cliente",addr[0],':',addr[1])
                msg25 = {"codigo":25,"msg":"Pokemones capturados","pokemones":lista_pokemones}
                conn.send(str(msg25).encode())

            if codigo == 31:
                print("Servidor: Recibí respuesta negativa de captura de pokemon del cliente",addr[0],':',addr[1])
                print("Servidor: Enviando mensaje de terminar sesión al cliente",addr[0],':',addr[1])
                msg32 = {"codigo":32,"msg":"Terminando sesión"}
                conn.send(str(msg32).encode())

            if codigo == 32:
                print("Servidor: Recibí solicitud de terminar sesión del cliente",addr[0],':',addr[1])
                msg32 = {"codigo":32,"msg":"Terminando sesión"}
                conn.send(str(msg32).encode())
                break
        else:
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
        print("Conexión establecida con", addr[0],':',addr[1])
        start_new_thread(threaded, (conn,addr))
        #sock.close()

if __name__ == '__main__':
	Main()
