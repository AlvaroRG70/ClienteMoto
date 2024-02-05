import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

class helper:

    def obtener_usuarios_select():
        # Obtenemos todos los usuarios
        headers = {'Authorization': 'Bearer ' + env("TOKEN_OAUTH")}
        response = requests.get('http://127.0.0.1:8000/api/v1/usuarios', headers=headers)
        usuarios = response.json()

        lista_usuarios = [("","Ninguna")]
        for usuario in usuarios:
            lista_usuarios.append((usuario["id"], usuario["nombre"]))  # Acceder a cada usuario individualmente
        return lista_usuarios
    
    def obtener_moto(id):
         # obtenemos todos los libros
        headers = {'Authorization': 'Bearer '+env("TOKEN_OAUTH")} 
        response = requests.get('http://127.0.0.1:8000/api/v1/motos/'+str(id),headers=headers)
        moto = response.json()
        return moto

