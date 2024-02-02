from django.shortcuts import render, redirect
from django.db.models import Q,Prefetch, Avg,Max,Min, F
from moto.forms import *
from django.contrib import messages
from datetime import datetime
import requests
from django.core import serializers
from pathlib import Path
import json
import xml.etree.ElementTree as ET

import environ
import os
env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))








# Create your views here.
def index(request):
    return render(request, 'index.html')

# def motos_lista_api(request):
#     response = requests.get('http://127.0.0.1:8000/api/v1/motos')
#     motos = parse_response(response)
#     return render(request, 'motos/lista_api.html',{'motos_mostrar':motos})


def parse_response(response):
    content_type = response.headers.get('Content-Type', '')
    
    if 'application/json' in content_type:
        return response.json()
    elif 'application/xml' in content_type:
        xml_data = response.content
        root = ET.fromstring(xml_data)
        return xml_to_dict(root)
    elif 'text/html' in content_type:
        # Manejar HTML si es necesario
        return response.text
    else:
        # Otros tipos de contenido
        return response.content


def xml_to_dict(xml_element):
    data = {}
    for child in xml_element:
        if child.tag in data:
            if isinstance(data[child.tag], list):
                data[child.tag].append(xml_to_dict(child))
            else:
                data[child.tag] = [data[child.tag], xml_to_dict(child)]
        else:
            data[child.tag] = xml_to_dict(child) if len(child) > 0 else child.text
    return data




def crear_cabecera():
    TOKEN =  env("TOKEN_OAUTH")
    return {'Authorization': f'Bearer {TOKEN}'}

#creamos una variable en el .env para ahorrarnos el poner la ruta y la versión en todos los lados si cambia


def crear_dominio():
    TOKEN =  env("RUTA")
    return TOKEN

def crear_version():
    TOKEN =  env("VERSION")
    return TOKEN

def motos_lista_api(request):
    
    headers = crear_cabecera()
    response = requests.get(crear_dominio() + crear_version() +'motos',  headers=headers)
    motos = parse_response(response)

    return render(request, 'motos/lista_api.html',{'motos_mostrar':motos})


def concesionarios_lista_api(request):
    
    headers = crear_cabecera()
    response = requests.get(crear_dominio() + crear_version() +'conc',  headers=headers)
    concesionarios = parse_response(response)
 
    return render(request, 'motos/lista_concesionarios.html',{'concesionarios_mostrar':concesionarios})


def eventos_lista_api(request):
     
    headers = crear_cabecera()
    response = requests.get(crear_dominio() + crear_version() +'eventos',  headers=headers)
    eventos = parse_response(response)

    return render(request, 'motos/lista_eventos.html',{'eventos_mostrar':eventos})







def moto_buscar_simple(request):
    
    formulario = MotoBusquedaForm(request.GET)
    
    if formulario.is_valid():
        headers = crear_cabecera()
        response = requests.get(
            crear_dominio() + crear_version() +'motos/busqueda_simple',  
            headers=headers,
            params=formulario.cleaned_data
        )
        
        motos = parse_response(response)
        print(motos)
        return render(request, 'motos/lista_api.html',{"motos_mostrar":motos})
    if("HTTP_REFERER" in request.META):
        return redirect(request.META["HTTP_REFERER"])
    else:
        return redirect("index")
    

from requests.exceptions import HTTPError
def moto_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaMotoForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                crear_dominio() + crear_version() +'motos/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                motos = parse_response(response)
                return render(request, 'motos/lista_api.html',
                              {"motos_mostrar":motos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = parse_response(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/busqueda_avanzada_moto.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaMotoForm(None)
    return render(request, 'motos/busqueda_avanzada_moto.html',{"formulario":formulario})



#Concesionario

def concesionario_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaConcesionarioForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                crear_dominio() + crear_version() +'concesionario/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                concesionarios = parse_response(response)
                return render(request, 'motos/lista_concesionarios.html',
                              {"concesionarios_mostrar":concesionarios})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = parse_response(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/busqueda_avanzada_concesionario.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaConcesionarioForm(None)
    return render(request, 'motos/busqueda_avanzada_concesionario.html',{"formulario":formulario})


def evento_busqueda_avanzada(request):
    if(len(request.GET) > 0):
        formulario = BusquedaAvanzadaEventoForm(request.GET)
        
        try:
            headers = crear_cabecera()
            response = requests.get(
                crear_dominio() + crear_version() +'evento/busqueda_avanzada',
                headers=headers,
                params=formulario.data
            )             
            if(response.status_code == requests.codes.ok):
                eventos = parse_response(response)
                return render(request, 'motos/lista_eventos.html',
                              {"eventos_mostrar":eventos})
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = parse_response(response)
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/busqueda_avanzada_evento.html',
                            {"formulario":formulario,"errores":errores})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = BusquedaAvanzadaEventoForm(None)
    return render(request, 'motos/busqueda_avanzada_evento.html',{"formulario":formulario})




#Páginas de Error
def mi_error_404(request,exception=None):
    return render(request, 'errores/404.html',None,None,404)

#Páginas de Error
def mi_error_500(request,exception=None):
    return render(request, 'errores/500.html',None,None,500)


