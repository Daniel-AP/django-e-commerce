from App.models import Producto, Resena
from django.core.mail import send_mail
from Tienda_Online import settings

class Productos:

    def todos(self,pagina):

        pagina += 1
        sql = Producto.objects.all().order_by("-calificacion")[(pagina-1)*15:pagina*15+1]

        self.__formato(sql)
        
        return sql

    def categoria(self,categoria_nombre,pagina):

        pagina += 1
        sql = (
            Producto.objects.filter(descuento__gt=0).order_by("-calificacion")[(pagina-1)*15:pagina*15+1]
            if categoria_nombre == "descuentos" else
            Producto.objects.filter(seccion=categoria_nombre).order_by("-calificacion")[(pagina-1)*15:pagina*15+1]
        )
        
        self.__formato(sql)

        return sql

    def producto(self,producto_codigo):

        sql = Producto.objects.filter(codigo_producto=producto_codigo)
        self.__formato(sql)

        return sql

    def buscar(self,request,pagina):

        pagina += 1
        sql = Producto.objects.raw("CALL BUSQUEDA(%s,%s);",(request.GET["busqueda"],(pagina-1)*15))

        self.__formato(sql)

        return sql

    def favoritos(self,request):

        sql = Producto.objects.raw("CALL FAVORITOS(%s)", (request.user.codigo_usuario,))
        self.__formato(sql)

        return sql

    def carrito(self,request):

        sql = Producto.objects.raw("CALL CARRITO(%s)",(request.user.codigo_usuario,))

        for i in sql: i.precio_total = (i.precio - ((i.precio*i.descuento)/100))*i.cantidad

        self.__formato(sql)

        return sql

    def calificaciones(self,codigo,pagina):

        pagina += 1
        sql = Resena.objects.filter(codigo_producto_id=codigo).order_by("-calificacion")[(pagina-1)*15:16]

        return sql

    def __formato(self,contenido):

        for i in contenido: i.precio = "{:,}".format(i.precio)        