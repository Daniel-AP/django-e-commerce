"""Tienda_Online URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from App.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('__debug__/', include('debug_toolbar.urls')),
    path('',inicio),
    path('tienda/<int:pagina>',tienda),
    path('contacto/',contacto),
    path('categoria/<str:nombre>/<int:pagina>',categoria),
    path('producto/<int:codigo>',producto),
    path('mas-resenas/<int:codigo>/<int:desde>',mas_resenas_producto),
    path('anadir-resena/<int:codigo>',anadir_resena),
    path('agregar-favorito/<int:codigo>',agregar_favorito),
    path('agregar-carrito/<int:codigo>',agregar_carrito),
    path('buscar/<int:pagina>',buscar),
    path('iniciosesion/',inicio_sesion),
    path('crearcuenta/',crear_cuenta),
    path('contrasena/',cambiar_contrasena),
    path('codigo-contrasena/',codigo_cambio_contrasena),
    path('perfil/',perfil_cuenta),
    path('salir/',salir_cuenta),
    path('infopersonal/<int:cambio>',info_personal),
    path('guardarinfo/',guardar_info),
    path('favoritos/',favoritos),
    path('carrito/',carrito),
    path('mas-producto-carrito/<int:codigo>',agregar_producto_carrito),
    path('menos-producto-carrito/<int:codigo>',eliminar_producto_carrito),
    path('borrar-producto-carrito/<int:codigo>',borrar_producto_carrito)
]
