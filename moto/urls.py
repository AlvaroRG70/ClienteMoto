from django.urls import path, re_path
from .import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path("motos/lista", views.motos_lista_api, name="motos_mostrar"),

]

