from django import template
from api.opciones import LISTA_HIMNOS
from api.models import Miembro

register = template.Library()

@register.filter
def himno(data, tipo):
    for value in data:
        if value.get("tipo") == tipo:
            return f"{LISTA_HIMNOS[value.get('numero')]}" 

@register.filter
def oracion(data, tipo):
    for value in data:
        print(value)
        if value.get("tipo") == tipo:
            nombre = Miembro.objects.get(pk=value.get("nombre_id"))
            return nombre.nombre
        
@register.filter
def discursante(id):
    if id:
        nombre = Miembro.objects.get(pk=id)
        return nombre.nombre
    else:
        return "Sin asignar"