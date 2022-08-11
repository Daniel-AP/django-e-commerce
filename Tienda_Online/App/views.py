import hashlib
import random
import string
from datetime import datetime
from math import ceil
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.utils import IntegrityError
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .logic import *
from .models import Carrito, Favorito, Usuario

productos = Productos()

def inicio(request):

    return render(request,"App/Inicio.html")

def contacto(request):

    if request.method == "GET":

        return render(request,"App/Contacto.html")

    else:

        send_mail(request.POST.get("asunto"),request.POST.get("cuerpo")+f"\n\n-{request.user.username}",settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER],fail_silently=False)

        return HttpResponse("")

def tienda(request,pagina):

    productos_todos = productos.todos(pagina)
    
    return render(request,"App/Tienda.html",{
        "productos_todos":productos_todos,
        "siguiente_pagina":pagina+1,
        "anterior_pagina":pagina-1,
        "pagina":pagina+1,
        "hay_siguiente_pagina":True if len(productos_todos) > 15 else False
    })

def categoria(request,nombre,pagina):

    categoria_contenido = productos.categoria(nombre,pagina)

    return render(request,"App/Categoria.html",{
        "categoria_contenido":categoria_contenido,
        "siguiente_pagina":pagina+1,
        "anterior_pagina":pagina-1,
        "nombre":nombre.capitalize(),
        "pagina":pagina+1,
        "hay_siguiente_pagina":True if len(categoria_contenido) > 15 else False
    })

def producto(request,codigo):

    if not request.user.is_anonymous:

        try:
            Favorito.objects.get(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo)
            es_favorito = True
        except Favorito.DoesNotExist:
            es_favorito = False

        es_carrito = True if Carrito.objects.filter(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo).exists() else False

        es_resena = True if Resena.objects.filter(codigo_producto_id=codigo,codigo_usuario_id=request.user.codigo_usuario).exists() else False
    
        resenas = Resena.objects.filter(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo).union(Resena.objects.filter(codigo_producto_id=codigo)[:10])

    else:
        resenas = Resena.objects.filter(codigo_producto_id=codigo)

    if resenas.exists():
        for i in resenas: i.fecha_resena = str(i.fecha_resena).replace("-","/")
    else:
        resenas = None

    return render(request,"App/Producto.html",{
        "producto_contenido":productos.producto(codigo),
        "es_favorito":es_favorito if not request.user.is_anonymous else None,
        "es_carrito":es_carrito if not request.user.is_anonymous else None,
        "es_resena":es_resena if not request.user.is_anonymous else None,
        "limite_resenas":Resena.objects.filter(codigo_producto_id=codigo).count(),
        "resenas":resenas,"fecha_actual":datetime.now().strftime("%Y-%m-%d").replace("-","/")
    })

def buscar(request,pagina):

    busqueda_contenido = productos.buscar(request,pagina)

    return render(request,"App/Busqueda.html",{
        "busqueda_contenido":busqueda_contenido,
        "siguiente_pagina":pagina+1,
        "anterior_pagina":pagina-1,
        "busqueda":request.GET["busqueda"],
        "pagina":pagina+1,
        "hay_siguiente_pagina":True if len(busqueda_contenido) > 15 else False
    })

@login_required(login_url="/iniciosesion")
def agregar_favorito(request,codigo):

    try:
        favorito_ = Favorito(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo)
        favorito_.save()
    except IntegrityError:
        favorito_ = Favorito.objects.get(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo)
        favorito_.delete()
        
    return HttpResponse("")

@login_required(login_url="/iniciosesion")
def agregar_carrito(request,codigo):

    carrito = Carrito(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo)
    carrito.save()

    return HttpResponse("")

def mas_resenas_producto(request,codigo,desde):

    mas_resenas = Resena.objects.filter(codigo_producto_id=codigo).exclude(codigo_producto_id=codigo,codigo_usuario_id=request.user.codigo_usuario)[desde:desde+10]

    return JsonResponse(serializers.serialize("json",mas_resenas),safe=False)

def anadir_resena(request,codigo):

    Resena(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo,resena_titulo=request.POST.get("titulo"),resena_texto=request.POST.get("texto"),calificacion=request.POST.get("calificacion")).save()

    producto_avg_calificaciones = (sum([i.calificacion for i in Resena.objects.filter(codigo_producto_id=codigo)])/len(Resena.objects.filter(codigo_producto_id=codigo)))
    producto_nueva_calificacion = ceil(producto_avg_calificaciones)
    producto = Producto.objects.get(codigo_producto=codigo)
    producto.calificacion = producto_nueva_calificacion
    producto.save()

    return HttpResponse("")

def inicio_sesion(request):

    if request.method == "GET":

        request.session["next"] = request.GET.get("next",request.session.get("next","/"))

    if request.method == "POST":

        usuario = authenticate(username=request.POST.get("nombre"), password=request.POST.get("contrasena"))

        if usuario is not None:

            login(request, usuario)
      
            return HttpResponse(request.session["next"])

        else:
            return HttpResponse("Error")
                
    return render(request,"App/Inicio_Sesion.html")

def crear_cuenta(request):

    if request.method == "GET":

        request.session["next"] = request.GET.get("next",request.session.get("next","/"))

    if request.method == "POST":

        try:

            usuario = Usuario.objects.create_user(username=request.POST.get("nombre"),password=request.POST.get("contrasena"),email=request.POST.get("email"))
            usuario.save()
            login(request, usuario)

            return HttpResponse(request.session["next"])

        except IntegrityError:

            return HttpResponse("Error")

    return render(request,"App/Crear_Cuenta.html")

@login_required(login_url="/iniciosesion")
def perfil_cuenta(request):

    return render(request,"App/Perfil.html")

def salir_cuenta(request):

    logout(request)

    return redirect("/")

def info_personal(request,cambio):
    
    return render(request,"App/Info_Personal.html",{"cambio":cambio})

def guardar_info(request):

    usuario = Usuario.objects.get(username=request.user.username)
    usuario.username = request.POST["nombre"]
    usuario.email = request.POST["email"]
    if not request.POST["contrasena"] == "********": usuario.set_password(request.POST["contrasena"])

    try:
        usuario.save()
    except IntegrityError:
        return render(request,"App/Info_Personal.html",{"error":"Este nombre de usuario ya ha sido usado.","cambio":1})

    logout(request)
    login(request,usuario)

    return redirect("/")

def cambiar_contrasena(request):

    if request.method == "POST":

        try:
            usuario = Usuario.objects.get(username=request.POST.get("nombre"),email=request.POST.get("email"))
    
            codigo = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))

            send_mail(
                "Cambio de contraseña - Tienda Online",
                "Hola, somos Tienda Online.\nPor favor introduzca el siguiente código para poder modificar su contraseña:\n\n%s" % codigo,
                settings.EMAIL_HOST_USER,
                [usuario.email],
                fail_silently=False
            )

            request.session["codigo"] = hashlib.sha256(codigo.encode()).hexdigest()
            request.session["username"] = usuario.username
            request.session["email"] = usuario.email

            return HttpResponse("/codigo-contrasena")

        except Usuario.DoesNotExist:

            return HttpResponse("Error")

    return render(request,"App/Contrasena.html")

def codigo_cambio_contrasena(request):

    if request.method == "GET":

        return render(request,"App/Codigo.html")

    else:

        if hashlib.sha256(request.POST.get("codigo","0").encode()).hexdigest() == request.session.get("codigo","0"):

            usuario = Usuario.objects.get(username=request.session["username"],email=request.session["email"])
            login(request,usuario)

            del request.session["codigo"],request.session["username"],request.session["email"]

            return HttpResponse("/infopersonal/1")

        else:

            return HttpResponse("Error")

def favoritos(request):

    favoritos_usuario = productos.favoritos(request)

    return render(request,"App/Favoritos.html",{
        "favoritos":favoritos_usuario
    })

def carrito(request):

    carrito_usuario = productos.carrito(request)
    subtotal = "{:,}".format(int(sum([i for i in map(lambda x: (int(x.precio.replace(",",""))-int(x.precio.replace(",",""))*x.descuento/100)*x.cantidad,carrito_usuario)])))

    return render(request,"App/Carrito.html",{
        "carrito":carrito_usuario,
        "subtotal":subtotal
    })

def agregar_producto_carrito(request,codigo):

    try:
        nuevo = Carrito.objects.create(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo)
        nuevo.save()
    except IntegrityError:
        nuevo = Carrito.objects.get(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo)
        nuevo.cantidad += 1
        nuevo.save()

    return HttpResponse("")

def eliminar_producto_carrito(request,codigo):

    eliminar = Carrito.objects.get(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo)
    eliminar.cantidad -= 1
    eliminar.save()

    return HttpResponse("")

def borrar_producto_carrito(request,codigo):

    eliminar = Carrito.objects.get(codigo_usuario_id=request.user.codigo_usuario,codigo_producto_id=codigo)
    eliminar.delete()

    return HttpResponse("")
