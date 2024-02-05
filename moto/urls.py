from django.urls import path, re_path
from .import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path("motos/lista", views.motos_lista_api, name="motos_mostrar"),
    path("motos/lista_conc", views.concesionarios_lista_api, name="concesionarios_mostrar"),
    path("motos/lista_eventos", views.eventos_lista_api, name="eventos_mostrar"),
    path('motos/buscar',views.moto_buscar_simple,name='moto_buscar'),
    path('motos/buscar_avanzado',views.moto_busqueda_avanzada,name='moto_buscar_avanzado'),
    path('concesionario/buscar_avanzado_conc',views.concesionario_busqueda_avanzada,name='concesionario_buscar_avanzado'),
    path('evento/buscar_avanzado_evento',views.evento_busqueda_avanzada,name='evento_buscar_avanzado'),
    path('moto/crear_moto',views.moto_crear,name='motos_crear'),
    path('moto/editar_moto/<int:moto_id>',views.moto_editar_nombre,name='motos_editar'),
    
    

]

