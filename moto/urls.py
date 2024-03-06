from django.urls import path, re_path
from .import views

urlpatterns = [
    path('',views.index,name = 'index'),
    path("motos/lista", views.motos_lista_api, name="motos_mostrar"),
    path('motos/<int:moto_id>',views.moto_obtener,name='moto_mostrar'),
    path("motos/lista_conc", views.concesionarios_lista_api, name="concesionarios_mostrar"),
    path("motos/lista_eventos", views.eventos_lista_api, name="eventos_mostrar"),
    path('motos/buscar',views.moto_buscar_simple,name='moto_buscar'),
    path('motos/buscar_avanzado',views.moto_busqueda_avanzada,name='moto_buscar_avanzado'),
    path('concesionario/buscar_avanzado_conc',views.concesionario_busqueda_avanzada,name='concesionario_buscar_avanzado'),
    path('evento/buscar_avanzado_evento',views.evento_busqueda_avanzada,name='evento_buscar_avanzado'),
    
    path('moto/crear_moto',views.moto_crear,name='motos_crear'),
    path('moto/editar_moto/<int:moto_id>',views.moto_editar,name='motos_editar'),
    path('moto/editar/nombre/<int:moto_id>',views.moto_editar_nombre,name='motos_editar_nombre'),
    path('moto/eliminar/<int:moto_id>',views.moto_eliminar,name='moto_eliminar'),
    
    path('concesionario/crear_concesionario',views.concesionario_crear,name='concesionarios_crear'),
    path('concesionario/editar_concesionario/<int:concesionario_id>',views.concesionario_editar,name='concesionarios_editar'),
    path('concesionario/editar/nombre/<int:concesionario_id>',views.concesionario_editar_nombre,name='concesionarios_editar_nombre'),
    path('concesionario/eliminar/<int:concesionario_id>',views.concesionario_eliminar,name='concesionario_eliminar'),
    
    path('evento/crear',views.evento_crear,name='eventos_crear'),
    path('evento/editar_evento/<int:evento_id>',views.evento_editar,name='evento_editar'),
    path('evento/editar/nombre/<int:evento_id>',views.evento_editar_nombre,name='eventos_editar_nombre'),
    path('evento/eliminar/<int:evento_id>',views.evento_eliminar,name='evento_eliminar'),
    
    #login
    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    
    
    path('valoracion/crear',views.valoracion_crear,name='valoraciones_crear'),
    
    path("motos/lista/caballos", views.motos_lista_caballos, name="motos_mostrar_caballos"),
    path("motos/reservar/<int:moto_id>", views.reservar_moto, name="motos_reservar"),
    
    
    
    
]

