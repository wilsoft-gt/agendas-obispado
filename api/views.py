import asyncio
from django.shortcuts import render, HttpResponse
from django.template.loader import get_template
from .models import Agenda, Discursante
from .utils import create_pdf
import threading
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

    pdf = create_pdf(html)
    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="Agenda_{agenda}.pdf"'
    
    return response

def discursante_pdf(request, pk):
    discursante = Discursante.objects.get(pk=pk)

    template= get_template("api/discurso.html")
    context = {"discursante": discursante}
    html = template.render(context)

    pdf = create_pdf(html)

    response = HttpResponse(pdf, content_type="application/pdf")
    response['Content-Disposition'] = f'attachment; filename="{"_".join(discursante.nombre.split(" "))}_{discursante.agenda}.pdf"'
    return response