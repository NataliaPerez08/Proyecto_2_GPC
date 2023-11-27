import requests
import random

def obtener_pokemon():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000&offset=0")
    r_json = response.json()
    n = random.randint(0, 1000)
    return r_json['results'][n]

def obtener_imagen_pokemon(pokemon):
    url_pokemon = pokemon['url']
    response = requests.get(url_pokemon)
    r_json = response.json()
    return r_json['sprites']['front_default']

def imprimir_pokemon():
    response = requests.get("https://pokeapi.co/api/v2/pokemon?limit=1000&offset=0")
    r_json = response.json()
    n = random.randint(0, 1000)    
    print(r_json['results'][n]['name'])
    url_pokemon = r_json['results'][n]['url']
    print(url_pokemon)

    response = requests.get(url_pokemon)
    r_json = response.json()
    print(r_json['name'])
    print(r_json['id'])
    print(r_json['sprites']['front_default'])

def ejemplos():
    print("Pokemon aleatorio")
    #imprimir_pokemon()
    pokemon=obtener_pokemon()
    print(pokemon['name'])
    imagen=obtener_imagen_pokemon(pokemon)
    print(imagen)