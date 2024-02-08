import requests
import environ
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)
env = environ.Env()


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
    
    def obtener_motos_select():

        headers = {'Authorization': 'Bearer ' + env("TOKEN_OAUTH")}
        response = requests.get('http://127.0.0.1:8000/api/v1/usuarios', headers=headers)
        motos = response.json()

        lista_motos = [("","Ninguna")]
        for moto in motos:
            lista_motos.append((moto["id"], moto["nombre"]))
        return lista_motos
    
    def obtener_moto(id):
         # obtenemos todos los libros
        headers = {'Authorization': 'Bearer '+env("TOKEN_OAUTH")} 
        response = requests.get('http://127.0.0.1:8000/api/v1/motos/'+str(id),headers=headers)
        print(response)
        moto = response.json()
        print('alli')
        print(moto)
        print('aqui')
        return moto
    
    def obtener_concesionario(id):

        headers = {'Authorization': 'Bearer '+env("TOKEN_OAUTH")} 
        response = requests.get('http://127.0.0.1:8000/api/v1/concesionario/'+str(id),headers=headers)
        concesionario = response.json()
        return concesionario
    
    
    
    
    def obtener_evento(id):

        headers = {'Authorization': 'Bearer '+env("TOKEN_OAUTH")} 
        response = requests.get('http://127.0.0.1:8000/api/v1/evento/'+str(id),headers=headers)
        evento = response.json()
        return evento
    
    
    

