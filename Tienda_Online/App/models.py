from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from datetime import datetime

class Usuario(AbstractUser):
    
    codigo_usuario = models.AutoField(primary_key=True)
    email = models.EmailField()
    last_login = models.DateTimeField(default=datetime.now)
    date_joined = models.DateTimeField(default=datetime.now)

    objects = UserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

class Producto(models.Model):

    codigo_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=35,db_index=True)
    seccion = models.CharField(max_length=30,db_index=True)
    precio = models.IntegerField()
    imagen_url = models.TextField()
    descripcion = models.TextField()
    descuento = models.IntegerField(default=0,db_index=True)
    calificacion = models.IntegerField(default=0,db_index=True)
    unidades = models.IntegerField()

class Resena(models.Model):

    codigo_resena = models.AutoField(primary_key=True)
    codigo_producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    codigo_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    resena_titulo = models.CharField(max_length=45)
    resena_texto = models.TextField()
    calificacion = models.IntegerField()
    fecha_resena = models.DateField(default=datetime.now().strftime("%Y-%m-%d"))

class Favorito(models.Model):

    codigo_favorito = models.AutoField(primary_key=True)
    codigo_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    codigo_producto = models.ForeignKey(Producto,on_delete=models.CASCADE)

class Carrito(models.Model):

    codigo_carrito = models.AutoField(primary_key=True)
    codigo_usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE)
    codigo_producto = models.ForeignKey(Producto,on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=1)
