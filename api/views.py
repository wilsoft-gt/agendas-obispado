from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from .models import Agenda, Discurso, Oracion

# Create your views here.

def render_agenda(request, pk):
    try:
        agenda = Agenda.objects.get(pk=pk)
        return render(request, "api/agenda.html", {"agenda": agenda})
    except Agenda.DoesNotExist:
        return render(request, "api/agenda.html")
    
def custom_login(request):
    return render(request, "api/login.html")
    
def agenda_pdf(request, pk):

    agenda = Agenda.objects.get(pk=pk)
    
    template = get_template("api/agenda.html")
    context = {"agenda": agenda}
    html = template.render(context)
    
    return HttpResponse(html)

def discursante_pdf(request, pk):
    discursante = Discurso.objects.get(pk=pk)

    template= get_template("api/discurso.html")
    context = {"discursante": discursante}
    html = template.render(context)

    return HttpResponse(html)

def oracion_pdf(request, pk):
    oracion = Oracion.objects.get(pk=pk)

    template = get_template("api/oracion.html")
    context = {"oracion": oracion}
    html = template.render(context)

    return HttpResponse(html)