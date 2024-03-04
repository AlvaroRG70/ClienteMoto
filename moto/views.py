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
environ.Env.read_env(os.path.join(BASE_DIR, '.env'),True)








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




def crear_cabecera(request):
    TOKEN =  request.session["token"]
    return {
        'Authorization': f'Bearer {TOKEN}',
        "Content-Type": "application/json"}


#creamos una variable en el .env para ahorrarnos el poner la ruta y la versión en todos los lados si cambia


def crear_dominio():
    TOKEN =  env("RUTA")
    return TOKEN

def crear_version():
    TOKEN =  env("VERSION")
    return TOKEN

def motos_lista_api(request):
    
    headers = crear_cabecera(request)
    print(headers)
    response = requests.get(crear_dominio() + crear_version() +'motos',  headers=headers)
    motos = parse_response(response)

    return render(request, 'motos/lista_api.html',{'motos_mostrar':motos})


def motos_lista_caballos(request):
    
    headers = crear_cabecera(request)
    print(headers)
    response = requests.get(crear_dominio() + crear_version() +'motos/caballos',  headers=headers)
    motos = parse_response(response)

    return render(request, 'motos/lista_motos_caballos.html',{'motos_mostrar_caballos':motos})


def moto_obtener(request,moto_id):
    moto = helper.obtener_moto(moto_id, request)
    return render(request, 'motos/moto_mostrar.html',{"moto":moto})


def concesionarios_lista_api(request):
    
    headers = crear_cabecera(request)
    response = requests.get(crear_dominio() + crear_version() +'conc',  headers=headers)
    concesionarios = parse_response(response)
 
    return render(request, 'motos/lista_concesionarios.html',{'concesionarios_mostrar':concesionarios})


def eventos_lista_api(request):
     
    headers = crear_cabecera(request)
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
            headers = crear_cabecera(request)
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
            headers = crear_cabecera(request)
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
            headers = crear_cabecera(request)
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


def moto_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = MotoForm(request.POST, request_usuario=request)
            headers =  {
                        'Authorization': 'Bearer '+ request.session["token"],
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            datos["usuarios"] = request.POST.getlist("usuariosDisponibles")
            
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/motos/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha creado la moto correctamente.')
                
                return redirect("motos_mostrar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/create_moto.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = MotoForm(None, request_usuario=request)
    return render(request, 'motos/create_moto.html',{"formulario":formulario})

def moto_editar(request,moto_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    moto = helper.obtener_moto(moto_id, request)
    formulario = MotoForm(datosFormulario,
            initial={
                'nombre': moto['nombre'],
                'modelo': moto['modelo'],
                'año': moto['año'],
                'imagen': moto['imagen'],
                'precio': moto['precio'],
                'marca': moto['marca'],

            }
        , request_usuario=request
    )
    if (request.method == "POST"):
        try:
            formulario = MotoForm(request.POST, request_usuario=request)
            headers = crear_cabecera(request)
            datos = request.POST.copy()
            datos["usuarios"] = request.POST.getlist("usuarios")             
            response = requests.put(
                'http://127.0.0.1:8000/api/v1/motos/editar/'+str(moto_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la moto correctamente.')
                return redirect("motos_mostrar")#,moto_id=moto_id
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/actualizar_moto.html',
                            {"formulario":formulario,"moto":moto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'motos/actualizar_moto.html',{"formulario":formulario,"moto":moto})


def moto_editar_nombre(request,moto_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    moto = helper.obtener_moto(moto_id, request)
    formulario = MotoActualizarNombreForm(datosFormulario,
            initial={
                'nombre': moto['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = MotoForm(request.POST, request_usuario=request)
            headers = crear_cabecera(request)
            datos = request.POST.copy()
            response = requests.patch(
                'http://127.0.0.1:8000/api/v1/motos/editar/nombre/'+str(moto_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado la moto correctamente.')
                return redirect("motos_mostrar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/actualizar_nombre_moto.html',
                            {"formulario":formulario,"moto":moto})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'motos/actualizar_nombre_moto.html',{"formulario":formulario,"moto":moto})


def moto_eliminar(request,moto_id):
    try:
        headers = crear_cabecera(request)
        response = requests.delete(
            'http://127.0.0.1:8000/api/v1/motos/eliminar/'+str(moto_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Se ha eliminado la moto correctamente.')
            
            return redirect("motos_mostrar")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('motos_mostrar')



def valoracion_crear(request):
    if request.method == "POST":
        try:
            formulario = ValoracionForm(request.POST, request_usuario=request)
            if formulario.is_valid():
                datos = formulario.cleaned_data
                # Acceder a los datos de los campos usuarios y concesionarios
                usuarios_seleccionados = datos.get("usuarios")
                concesionarios_seleccionados = datos.get("concesionarios")
                
                # Resto del código para enviar los datos al servidor...
                headers = {
                    'Authorization': 'Bearer ' + request.session["token"],
                    "Content-Type": "application/json"
                }
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/valoraciones/crear',
                    headers=headers,
                    data=json.dumps(datos)
                )
                if response.status_code == requests.codes.ok:
                    messages.success(request, 'Se ha creado la valoración correctamente.')
                    return redirect("concesionarios_mostrar")
                else:
                    print(response.status_code)
                    response.raise_for_status()
            else:
                errores = formulario.errors
                return render(request, 'motos/create_valoracion.html', {"formulario": formulario, "errores": errores})
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, 'motos/create_valoracion.html', {"formulario": formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    else:
        formulario = ValoracionForm(request_usuario=request)
    return render(request, 'motos/create_valoracion.html', {"formulario": formulario})









def concesionario_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = ConcesionarioForm(request.POST, request_moto=request)
            headers =  {
                        'Authorization': 'Bearer '+ request.session["token"],
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            datos["motos"] = request.POST.getlist("motosDisponibles")
            datos["fecha_apertura"] = str(date(year=int(datos['fecha_apertura_year']),
                                                        month=int(datos['fecha_apertura_month']),
                                                        day=int(datos['fecha_apertura_day'])))
            
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/concesionario/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha creado el concesionario correctamente.')
                return redirect("concesionarios_mostrar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/create_concesionario.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = ConcesionarioForm(None, request_moto=request)
    return render(request, 'motos/create_concesionario.html',{"formulario":formulario})


def concesionario_editar(request,concesionario_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    concesionario = helper.obtener_concesionario(concesionario_id, request)
    formulario = ConcesionarioForm(datosFormulario,
            initial={
                'nombre': concesionario['nombre'],
                'descripcion': concesionario['descripcion'],
                'ubicacion': concesionario['ubicacion'],
                'telefono': concesionario['telefono'],
                'fecha_apertura': datetime.strptime(concesionario['fecha_apertura'], '%Y-%m-%d').date(),
                
            }
            ,request_moto=request
    )
    if (request.method == "POST"):
        try:
            formulario = ConcesionarioForm(request.POST, request_moto=request)
            headers = crear_cabecera(request)
            datos = request.POST.copy()
              
            datos["fecha_apertura"] = str(date(year=int(datos['fecha_apertura_year']),
                                                        month=int(datos['fecha_apertura_month']),
                                                        day=int(datos['fecha_apertura_day'])))
            
            response = requests.put(
                'http://127.0.0.1:8000/api/v1/concesionario/editar/'+str(concesionario_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado el concesionario correctamente.')
                
                return redirect("concesionarios_mostrar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/actualizar_concesionario.html',
                            {"formulario":formulario,"concesionario":concesionario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'motos/actualizar_concesionario.html',{"formulario":formulario,"concesionario":concesionario})



def concesionario_editar_nombre(request,concesionario_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    concesionario = helper.obtener_concesionario(concesionario_id, request)
    formulario = ConcesionarioActualizarNombreForm(datosFormulario,
            initial={
                'nombre': concesionario['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = ConcesionarioForm(request.POST, request_moto=request)
            headers = crear_cabecera(request)
            datos = request.POST.copy()
            response = requests.patch(
                'http://127.0.0.1:8000/api/v1/concesionario/editar/nombre/'+str(concesionario_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado el concesionario correctamente.')
                
                return redirect("concesionarios_mostrar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/actualizar_nombre_concesionario.html',
                            {"formulario":formulario,"concesionario":concesionario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'motos/actualizar_nombre_concesionario.html',{"formulario":formulario,"concesionario":concesionario})



def concesionario_eliminar(request,concesionario_id):
    try:
        headers = crear_cabecera(request)
        response = requests.delete(
            'http://127.0.0.1:8000/api/v1/concesionario/eliminar/'+str(concesionario_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Se ha eliminado el concesionario correctamente.')
            
            return redirect("concesionarios_mostrar")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('concesionarios_mostrar')




def evento_crear(request):
    
    if (request.method == "POST"):
        try:
            formulario = EventoForm(request.POST, request_usuario=request)
            headers =  {
                        'Authorization': 'Bearer '+request.session["token"],
                        "Content-Type": "application/json" 
                    } 
            datos = formulario.data.copy()
            datos["usuarios"] = request.POST.getlist("usuariosDisponibles")
            datos["fecha"] = str(date(year=int(datos['fecha_year']),
                                                        month=int(datos['fecha_month']),
                                                        day=int(datos['fecha_day'])))
            
            response = requests.post(
                'http://127.0.0.1:8000/api/v1/evento/crear',
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                
                messages.success(request, 'Se ha creado el evento correctamente.')
                return redirect("eventos_mostrar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/create_evento.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
        
    else:
         formulario = EventoForm(None,request_usuario= request)
    return render(request, 'motos/create_evento.html',{"formulario":formulario})


def evento_editar(request,evento_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    evento = helper.obtener_evento(evento_id,request)
    formulario = EventoForm(datosFormulario,
            initial={
                'nombre': evento['nombre'],
                'descripcion': evento['descripcion'],
                'ubicacion': evento['ubicacion'],
                'hora': evento['hora'],
                'kms': evento['kms'],
                'fecha': datetime.strptime(evento['fecha'], '%Y-%m-%d').date(),
                
            }
            , request_usuario=request
    )
    
    if (request.method == "POST"):
        try:
            formulario = EventoForm(request.POST, request_usuario=request)
            headers = crear_cabecera(request)
            datos = request.POST.copy()
              
            datos["fecha"] = str(date(year=int(datos['fecha_year']),
                                                        month=int(datos['fecha_month']),
                                                        day=int(datos['fecha_day'])))
            
            response = requests.put(
                'http://127.0.0.1:8000/api/v1/evento/editar/'+str(evento_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                
                messages.success(request, 'Se ha editado el evento correctamente.')
                return redirect("eventos_mostrar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/actualizar_evento.html',
                            {"formulario":formulario,"evento":evento})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'motos/actualizar_evento.html',{"formulario":formulario,"evento":evento})



def evento_editar_nombre(request,evento_id):
   
    datosFormulario = None
    
    if request.method == "POST":
        datosFormulario = request.POST
    
    evento = helper.obtener_evento(evento_id, request)
    formulario = EventoActualizarNombreForm(datosFormulario,
            initial={
                'nombre': evento['nombre'],
            }
    )
    if (request.method == "POST"):
        try:
            formulario = EventoForm(request.POST, request_usuario=request)
            headers = crear_cabecera(request)
            datos = request.POST.copy()
            response = requests.patch(
                'http://127.0.0.1:8000/api/v1/evento/editar/nombre/'+str(evento_id),
                headers=headers,
                data=json.dumps(datos)
            )
            if(response.status_code == requests.codes.ok):
                messages.success(request, 'Se ha editado el evento correctamente.')
                
                return redirect("eventos_mostrar")
            else:
                print(response.status_code)
                response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'motos/actualizar_nombre_evento.html',
                            {"formulario":formulario,"evento":evento})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
    return render(request, 'motos/actualizar_nombre_evento.html',{"formulario":formulario,"evento":evento})



def evento_eliminar(request,evento_id):
    try:
        headers = crear_cabecera(request)
        response = requests.delete(
            'http://127.0.0.1:8000/api/v1/evento/eliminar/'+str(evento_id),
            headers=headers,
        )
        if(response.status_code == requests.codes.ok):
            messages.success(request, 'Se ha eliminado el evento correctamente.')
            
            return redirect("eventos_mostrar")
        else:
            print(response.status_code)
            response.raise_for_status()
    except Exception as err:
        print(f'Ocurrió un error: {err}')
        return mi_error_500(request)
    return redirect('eventos_mostrar')




def registrar_usuario(request):
    if (request.method == "POST"):
        try:
            formulario = RegistroForm(request.POST)
            if(formulario.is_valid()):
                headers =  {
                            "Content-Type": "application/json" 
                        }
                response = requests.post(
                    'http://127.0.0.1:8000/api/v1/registrar/usuario',
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )
                
                if(response.status_code == requests.codes.ok):
                    usuario = response.json()
                    token_acceso = helper.obtener_token_session(
                            formulario.cleaned_data.get("username"),
                            formulario.cleaned_data.get("password1")
                            )
                    request.session["usuario"]=usuario
                    request.session["token"] = token_acceso
                    return redirect("index")
                else:
                    print(response.status_code)
                    response.raise_for_status()
        except HTTPError as http_err:
            print(f'Hubo un error en la petición: {http_err}')
            if(response.status_code == 400):
                errores = response.json()
                for error in errores:
                    formulario.add_error(error,errores[error])
                return render(request, 
                            'registration/signup.html',
                            {"formulario":formulario})
            else:
                return mi_error_500(request)
        except Exception as err:
            print(f'Ocurrió un error: {err}')
            return mi_error_500(request)
            
    else:
        formulario = RegistroForm()
    return render(request, 'registration/signup.html', {'formulario': formulario})

def login(request):
    if (request.method == "POST"):
        formulario = LoginForm(request.POST)
        try:
            token_acceso = helper.obtener_token_session(
                                formulario.data.get("usuario"),
                                formulario.data.get("password")
                                )
            request.session["token"] = token_acceso
            
          
            headers = {'Authorization': 'Bearer '+token_acceso} 
            response = requests.get('http://127.0.0.1:8000/api/v1/usuario/token/'+token_acceso,headers=headers)
            usuario = response.json()
            request.session["usuario"] = usuario
            
            return  redirect("index")
        except Exception as excepcion:
            print(f'Hubo un error en la petición: {excepcion}')
            formulario.add_error("usuario",excepcion)
            formulario.add_error("password",excepcion)
            return render(request, 
                            'registration/login.html',
                            {"form":formulario})
    else:  
        formulario = LoginForm()
    return render(request, 'registration/login.html', {'form': formulario})


    
def logout(request):
    del request.session['token']
    return redirect('index')