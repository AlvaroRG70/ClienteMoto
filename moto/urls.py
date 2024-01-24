from django.urls import path, re_path
from .import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path("motos/lista", views.motos_lista_api, name="motos_mostrar"),
    path("motos/lista_conc", views.concesionarios_lista_api, name="concesionarios_mostrar"),
    path("motos/lista_eventos", views.eventos_lista_api, name="eventos_mostrar"),
    path('motos/buscar',views.moto_buscar_simple,name='moto_buscar'),

]

