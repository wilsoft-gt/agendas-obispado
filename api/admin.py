from django.contrib import admin
from django.utils.html import format_html
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import Obispado, Organizacion, Templo, Entrevista, Limpieza, Asunto, Actividad, Agenda, Himno, Oracion, Discursante
# Register your models here.

admin.site.site_header = "Barrio Pinares 1"
admin.site.site_title = "Barrio Pianres 1"
admin.site.register(Obispado)
admin.site.register(Organizacion)
admin.site.register(Templo)
admin.site.register(Entrevista)
admin.site.register(Limpieza)
admin.site.register(Asunto)
admin.site.register(Actividad)


class HimnoInline(admin.TabularInline):
	model=Himno
	extra = 1


class DiscursanteInline(admin.TabularInline):
	model=Discursante
	extra=1
	max_num=5

	def descargar(self, obj):
		if obj.pk is not None:
			return format_html(f'<a class="btn btn-warning" href="/discurso/{obj.pk}/">Descargar pdf</a>')
		else:
			return format_html('<span></span>')
	descargar.short_description = "Carta"
	readonly_fields = ("descargar",)


class OracionInline(admin.TabularInline):
	model=Oracion
	max_num=2
	verbose_name="Oracion"
	verbose_name_plural="Oraciones"

	def descargar(self, obj):
		if obj.pk is not None:
			return format_html(f'<a class="btn btn-warning" href="/oracion/{obj.pk}/">Descargar pdf</a>')
		else:
			return format_html('<span></span>')
		
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
		DiscursanteInline,
		AsuntoInline,
		ActividadInline,
		TemploInline,
	]

	def descargar(self, obj):
		return format_html(f'<a class="btn btn-warning" href="/agenda-pdf/{obj.pk}/">Descargar pdf</a>')
  
	descargar.short_description = "Agenda"
	list_display = ['fecha', 'descargar']
	search_fields = ['fecha']

admin.site.register(Agenda,AgendaAdmin)