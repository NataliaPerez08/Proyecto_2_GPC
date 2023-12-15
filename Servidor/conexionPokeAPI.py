import requests
import random

# Obtiene la imagen de un pokemon de la API. Retorna un objeto response de requests 
# (imagen en bytes)
def obtener_imagen_pokemon(pokemon):
    id = pokemon['id']
    url_pokemon= "https://pokeapi.co/api/v2/pokemon/"+str(id)
    response = requests.get(url_pokemon)
    r_json = response.json()
    image_url = r_json['sprites']['front_default']
    response = requests.get(image_url)
    return response

# Genera un numero aleatorio entre 1 y 255, para obtener un pokemon aleatorio
# de la API. Retorna un diccionario con los datos del pokemon.
def obtener_pokemon():
    id = random.randint(1, 255)
    #GET https://pokeapi.co/api/v2/pokemon/{id or name}/
    response = requests.get("https://pokeapi.co/api/v2/pokemon/"+str(id))
    r_json = response.json()
    return r_json
