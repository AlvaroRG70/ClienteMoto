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
    response = requests.get('http://127.0.0.1:8000/api/v1/motos')
    motos = response.json()
    return render(request, 'motos/lista_api.html',{'motos_mostrar':motos})



