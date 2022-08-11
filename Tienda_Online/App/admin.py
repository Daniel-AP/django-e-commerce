from django.contrib import admin
from App.models import *

# Register your models here.

class ProductoAdmin(admin.ModelAdmin):

    list_display = ("codigo_producto","nombre_producto","precio","seccion","descuento","unidades")
    list_filter = ("precio","seccion","descuento","unidades")
    search_fields = ("codigo_producto","nombre_producto")

class FavoritoAdmin(admin.ModelAdmin):

    list_display = ("codigo_favorito","codigo_producto")
    list_filter = ("codigo_producto",)
    search_fields = ("codigo_favorito",)

class CarritoAdmin(admin.ModelAdmin):

    list_display = ("codigo_carrito","codigo_producto")
    list_filter = ("codigo_producto",)
    search_fields = ("codigo_carrito",)

class UsuarioAdmin(admin.ModelAdmin):

    list_display = ("codigo_usuario","username","email")
    list_filter = ("email",)
    search_fields = ("codigo_usuario","email","username")

admin.site.register(Producto,ProductoAdmin)
admin.site.register(Favorito,FavoritoAdmin)
admin.site.register(Carrito,CarritoAdmin)
admin.site.register(Usuario,UsuarioAdmin)