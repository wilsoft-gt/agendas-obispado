from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.html import format_html
from .models import Obispado, Organizacion, Templo, Limpieza, Asunto, Actividad, Agenda, Himno, Oracion, Discurso, Miembro
from datetime import datetime
# Register your models here.

admin.site.site_header = "Barrio Pinares 1"
admin.site.site_title = "Barrio Pianres 1"
admin.site.register(Obispado)
admin.site.register(Organizacion)
admin.site.register(Asunto)
admin.site.register(Actividad)



def calcular_fechas(fecha):
	delta = datetime.today().date() - fecha
	años = int(delta.days / 365)
	meses = int(delta.days / 30)
	semanas = int(delta.days / 7)
	if (años > 0):
		if (años == 1):
			return f'{años} año'
		else:
			return f'{años} años'
	if (meses > 0):
		if meses == 1:
			return f'{meses} mes'
		else:
			return f'{meses} meses'
	if (semanas > 0):
		if semanas == 1:
			return f'{semanas} semana'
		else:
			return f'{semanas} semanas'
	if delta.days == 1:
		return f'{delta.days} dia'
	else:
		return f'{delta.days} dias'


class MiembroAdmin(admin.ModelAdmin):
	model=Miembro
	def ultimoDiscurso(self, obj):
		discursos = obj.discurso_set.all()
		if obj.pk is not None and discursos:
			fecha = discursos.order_by("-agenda")[0].agenda.fecha
			return format_html(f'<span>Hace {calcular_fechas(fecha)} ({fecha})</span>')
		else:
			return format_html(f'<span>No ha discursado</span>')

	def ultimoDiscursoTema(self, obj):
		discurso = obj.discurso_set.all()
		if obj.pk is not None and discurso:
			print(discurso.order_by("-agenda")[0].tema)
			return format_html(f'<span>{discurso.order_by("-agenda")[0].tema}</span>')
		else:
			return format_html("<span>Sin datos</span>")
	
	def ultimaOracion(self, obj):
		oraciones = obj.oracion_set.all()
		if obj.pk is not None and oraciones:
			fecha = oraciones.order_by("-agenda")[0].agenda.fecha
			return format_html(f'<span>Hace {calcular_fechas(fecha)} ({fecha})</span>')
		else:
			return format_html(f'<span>No ha orado</span>')
	ultimoDiscurso.short_description = "Ultimo Discurso"
	ultimaOracion.short_description = "Ultima Oracion"
	ultimoDiscursoTema.short_description = "Tema"
	list_display = ["nombre", "ultimoDiscurso", "ultimoDiscursoTema", "ultimaOracion"]

admin.site.register(Miembro,MiembroAdmin)


class HimnoInline(admin.TabularInline):
	model=Himno
	extra = 1


class DiscursoInline(admin.TabularInline):
	model=Discurso
	extra=1
	max_num=5

	def descargar(self, obj):
		if obj.pk is not None:
			return format_html(f'<a class="btn btn-warning" href="/discurso/{obj.pk}/" target="_blank">Descargar pdf</a>')
		else:
			return format_html('<span>Sin guardar</span>')
	descargar.short_description = "Carta"
	readonly_fields = ("descargar",)


class OracionInline(admin.TabularInline):
	model=Oracion
	max_num=2
	verbose_name="Oracion"
	verbose_name_plural="Oraciones"

	def descargar(self, obj):
		if obj.pk is not None:
			return format_html(f'<a class="btn btn-warning" href="/oracion/{obj.pk}/" target="_blank">Descargar pdf</a>')
		else:
			return format_html('<span>Sin guardar</span>')
		
	descargar.short_description="Carta"
	readonly_fields = ("descargar",)


class ActividadInline(admin.TabularInline):
	model=Actividad.agenda.through
	extra = 1
	verbose_name = "Actividad"
	verbose_name_plural = "Actividades"


class AsuntoInline(admin.TabularInline):
	model=Asunto.agenda.through
	verbose_name = "Asunto"
	verbose_name_plural = "Asuntos"

class TemploInline(admin.TabularInline):
	model=Templo.agenda.through
	verbose_name = "Visita al templo"
	verbose_name_plural = "Visitas al templo"
	extra = 1


class AgendaAdmin(admin.ModelAdmin): 
	inlines = [
		HimnoInline,
		OracionInline,
		DiscursoInline,
		AsuntoInline,
		ActividadInline,
		TemploInline,
	]

	def descargar(self, obj):
		return format_html(f'<a class="btn btn-warning" href="/agenda-pdf/{obj.pk}/" target="_blank">Descargar pdf</a>')
  
	descargar.short_description = "Agenda"
	list_display = ['fecha', 'descargar']
	search_fields = ['fecha']

admin.site.register(Agenda,AgendaAdmin)