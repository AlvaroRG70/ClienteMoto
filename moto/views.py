from django.shortcuts import render, redirect
from django.db.models import Q,Prefetch, Avg,Max,Min, F
from moto.forms import *
from django.contrib import messages
from datetime import datetime
import requests
from django.core import serializers

# Create your views here.
def index(request):
    return render(request, 'index.html')

def motos_lista_api(request):
    response = requests.get('http://127.0.0.1:8000/api/v1/motos')
    motos = response.json()
    return render(request, 'motos/lista_api.html',{'motos_mostrar':motos})

def motos_lista_api(request):
    
    headers = {'Authorization': 'Bearer iOoL411h1OAgx14jRmgAebvcbPBmYt'}
    response = requests.get('http://127.0.0.1:8000/api/v1/motos',  headers=headers)
    motos = response.json()

    return render(request, 'motos/lista_api.html',{'motos_mostrar':motos})




def concesionarios_lista_api(request):
    
    headers = {'Authorization': 'Bearer iOoL411h1OAgx14jRmgAebvcbPBmYt'}
    response = requests.get('http://127.0.0.1:8000/api/v1/conc',  headers=headers)
    concesionarios = response.json()
 
    return render(request, 'motos/lista_concesionarios.html',{'concesionarios_mostrar':concesionarios})


def eventos_lista_api(request):
    
    headers = {'Authorization': 'Bearer iOoL411h1OAgx14jRmgAebvcbPBmYt'}
    response = requests.get('http://127.0.0.1:8000/api/v1/eventos',  headers=headers)
    eventos = response.json()

    return render(request, 'motos/lista_eventos.html',{'eventos_mostrar':eventos})




def crear_cabecera():
    return {'Authorization': 'Bearer iOoL411h1OAgx14jRmgAebvcbPBmYt'}


def moto_buscar_simple(request):
    
    formulario = MotoBusquedaForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            'http://127.0.0.1:8000/api/v1/motos/busqueda_simple',  
            headers=headers,
            params=formulario.cleaned_data
        )
        
        motos = response.json()
        print(motos)
        return render(request, 'motos/lista_api.html',{"motos_mostrar":motos})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    


