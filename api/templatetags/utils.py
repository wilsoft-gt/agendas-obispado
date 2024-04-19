from django import template
from api.opciones import LISTA_HIMNOS

register = template.Library()

@register.filter
def himno(data, tipo):
    for value in data:
        if value.get("tipo") == tipo:
            return f"{LISTA_HIMNOS[value.get('numero')]}" 

@register.filter
def oracion(data, tipo):
    for value in data:
        if value.get("tipo") == tipo:
            return f"{value.get('nombre')}"