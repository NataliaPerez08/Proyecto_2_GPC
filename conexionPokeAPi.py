import requests
import random

def obtener_imagen_pokemon(pokemon):
    id = pokemon['id']
    url_pokemon= "https://pokeapi.co/api/v2/pokemon/"+str(id)
    response = requests.get(url_pokemon)
    r_json = response.json()
    return r_json['sprites']['front_default']

def ejemplos():
    print("Pokemon aleatorio")
    pokemon=obtener_pokemon_por_id()
    id = pokemon['id']
    print(pokemon['id'])
    print(pokemon['name'])
    imagen_url=obtener_imagen_pokemon(pokemon)
    response = requests.get(imagen_url)
    with open('pr.png', 'wb') as handler:
        handler.write(response.content)

def obtener_pokemon_por_id():
    id = random.randint(1, 1000)
    #GET https://pokeapi.co/api/v2/pokemon/{id or name}/
    response = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(id))
    r_json = response.json()
    return r_json

ejemplos()