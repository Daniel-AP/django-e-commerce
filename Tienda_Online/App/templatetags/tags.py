from django import template

register = template.Library()

@register.filter(name="t_range")
def t_range(num):
    return range(num)

@register.filter(name="t_precio_descuento")
def t_precio_descuento(num1,num2):
    num1 = int((num1.replace(".","").replace(",","")))

    return "{:,}".format(num1 - int(num1 * num2 / 100))