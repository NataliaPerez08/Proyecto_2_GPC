import socket
import random
import conexionPokeAPi  as pokeapi
from _thread import start_new_thread
def threaded(conn, addr):
  
    pokemon_actual = ""
    lista_pokemones = []
    intentos = 5 # Valor inicial
    while True:
        # Recibe un mensaje del cliente
        data = conn.recv(1024)
        if data: 
            try:
                codigo = int.from_bytes(data, byteorder='big')
            except SyntaxError:
                print("Servidor: Recibí mensaje inválido del cliente",addr[0],':',addr[1])

            if codigo == 10:
                print("Servidor: Recibí solicitud de pokemon")
                pokemon_actual = pokeapi.obtener_pokemon()
                id_pokemon = pokemon_actual['id']
                print("Elección de pokemon: ",id_pokemon,".-",pokemon_actual['name'], )

                print("Servidor: Enviando pokemon al cliente",addr[0],':',addr[1])
                # {"codigo":20,"msg":"¿Capturar pokemon?","pokemon":pokemon_actual} 
                codigo_byte = int.to_bytes(20, length=1, byteorder='big')
                msg20_byte = int.to_bytes(id_pokemon, length=1, byteorder='big')
                # concatena los bytes [code,idPokemon]
                msg_byte = codigo_byte + msg20_byte
                conn.send(msg_byte)

            if codigo == 30:
                print("Servidor: Recibí respuesta afirmativa de captura de pokemon del cliente",addr[0],':',addr[1])
                capturado = random.randint(0,2)

                if capturado == 1:
                    print("Servidor: Pokemon capturado del cliente",addr[0],':',addr[1], ". Enviando...")
                    lista_pokemones.append(pokemon_actual['id'])
                    #{"codigo":22,"msg":"Pokemon capturado","pokemon":pokemon_actual}
                    # [code,idPokemon,imageSize,image]
                    codigo_byte = int.to_bytes(22, length=1, byteorder='big')
                    id_pokemon_byte = int.to_bytes(pokemon_actual['id'], length=1, byteorder='big')
                    imagen_pokemon = pokeapi.obtener_imagen_pokemon(pokemon_actual)
                    imagen_pokemon_byte = imagen_pokemon.content
                    print("Tamaño de imagen: ",len(imagen_pokemon_byte))
                    image_size_byte = int.to_bytes(len(imagen_pokemon_byte), length=4, byteorder='big')
                    msg_byte = codigo_byte + id_pokemon_byte + image_size_byte + imagen_pokemon_byte
                    conn.send(msg_byte)
                else:
                    print("Servidor: Pokemon no capturado del cliente",addr[0],':',addr[1])
                    intentos = intentos - 1
                    if intentos == 0:
                        print("Servidor: Intentos de captura agotados")
                        #{"codigo":23,"msg":"Intentos de captura agotados"}
                        codigo_byte = int.to_bytes(23, length=1, byteorder='big')
                        conn.send(codigo_byte)
                    else:
                        #{"codigo":21,"msg":"¿Intentar captura de nuevo?","intentos":intentos}
                        codigo_byte = int.to_bytes(21, length=1, byteorder='big')
                        id_pokemon_byte = int.to_bytes(pokemon_actual['id'], length=1, byteorder='big')
                        intentos_byte = int.to_bytes(intentos, length=1, byteorder='big')
                        msg_byte = codigo_byte + id_pokemon_byte + intentos_byte
                        conn.send(msg_byte)
            if codigo == 24:
                print("Servidor: Recibí solicitud de pokemones capturados del cliente",addr[0],':',addr[1])
                #msg25 = {"codigo":25,"msg":"Pokemones capturados","pokemones":lista_pokemones}
                codigo_byte = int.to_bytes(25, length=1, byteorder='big')
                s_lista_pokemones = str(lista_pokemones)
                # convierte la lista de pokemones a bytes
                bytes_lista_pokemones = s_lista_pokemones.encode()
                print(s_lista_pokemones)
                print(bytes_lista_pokemones)
                msg_byte = codigo_byte + bytes_lista_pokemones
                conn.send(msg_byte)

            if codigo == 31:
                print("Servidor: Recibí respuesta negativa de captura de pokemon del cliente",addr[0],':',addr[1])
                print("Servidor: Enviando mensaje de terminar sesión al cliente",addr[0],':',addr[1])
                #{"codigo":32,"msg":"Terminando sesión"}
                codigo_byte = int.to_bytes(32, length=1, byteorder='big')
                conn.send(codigo_byte)

            if codigo == 32:
                print("Servidor: Recibí solicitud de terminar sesión del cliente",addr[0],':',addr[1])
                codigo_byte = int.to_bytes(32, length=1, byteorder='big')
                conn.send(codigo_byte)
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
