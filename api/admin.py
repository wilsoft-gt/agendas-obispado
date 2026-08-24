from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.html import format_html
from django.db.models import OuterRef, Subquery
from .models import Obispado, Organizacion, Templo, Limpieza, Asunto, Actividad, Agenda, Himno, Oracion, Discurso, Miembro
from datetime import datetime
# Register your models here.

admin.site.site_header = "Barrio Pinares 1"
admin.site.site_title = "Barrio Pianres 1"
admin.site.register(Obispado)
admin.site.register(Organizacion)


class AsuntoAdmin(admin.ModelAdmin):
	search_fields = ['titulo', 'descripcion', 'organizacion__nombre']


class TemploAdmin(admin.ModelAdmin):
	search_fields = ['observaciones', 'reservado_por__nombre']


admin.site.register(Asunto, AsuntoAdmin)
admin.site.register(Templo, TemploAdmin)


class ActividadAdmin(admin.ModelAdmin):
	search_fields = ['titulo', 'lugar', 'organizacion__nombre']


admin.site.register(Actividad, ActividadAdmin)



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
	model = Miembro
	search_fields = ['nombre']

	def get_queryset(self, request):
		queryset = super().get_queryset(request)
		latest_discurso = Discurso.objects.filter(
			nombre=OuterRef('pk'), agenda__isnull=False
		).order_by('-agenda__fecha')
		latest_oracion = Oracion.objects.filter(
			nombre=OuterRef('pk'), agenda__isnull=False
		).order_by('-agenda__fecha')
		return queryset.annotate(
			ultimo_discurso_fecha=Subquery(latest_discurso.values('agenda__fecha')[:1]),
			ultimo_discurso_tema=Subquery(latest_discurso.values('tema')[:1]),
			ultima_oracion_fecha=Subquery(latest_oracion.values('agenda__fecha')[:1]),
		)

	def ultimoDiscurso(self, obj):
		fecha = getattr(obj, 'ultimo_discurso_fecha', None)
		if fecha:
			return format_html(f'<span>Hace {calcular_fechas(fecha)} ({fecha})</span>')
		return format_html('<span>No ha discursado</span>')

	def ultimoDiscursoTema(self, obj):
		tema = getattr(obj, 'ultimo_discurso_tema', None)
		if tema:
			return format_html(f'<span>{tema}</span>')
		return format_html('<span>Sin datos</span>')
	
	def ultimaOracion(self, obj):
		fecha = getattr(obj, 'ultima_oracion_fecha', None)
		if fecha:
			return format_html(f'<span>Hace {calcular_fechas(fecha)} ({fecha})</span>')
		return format_html('<span>No ha orado</span>')

	ultimoDiscurso.admin_order_field = 'ultimo_discurso_fecha'
	ultimoDiscursoTema.admin_order_field = 'ultimo_discurso_tema'
	ultimaOracion.admin_order_field = 'ultima_oracion_fecha'
	ultimoDiscurso.short_description = "Ultimo Discurso"
	ultimaOracion.short_description = "Ultima Oracion"
	ultimoDiscursoTema.short_description = "Tema"
	list_display = ["nombre", "ultimoDiscurso", "ultimoDiscursoTema", "ultimaOracion"]

admin.site.register(Miembro,MiembroAdmin)


class HimnoInline(admin.TabularInline):
	model=Himno
	extra = 0


class DiscursoInline(admin.TabularInline):
	model=Discurso
	extra=0
	max_num=5
	autocomplete_fields = ['nombre']

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
	autocomplete_fields = ['nombre']
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
	autocomplete_fields = ['actividad']

class AsuntoInline(admin.TabularInline):
	model=Asunto.agenda.through
	extra = 0
	autocomplete_fields = ['asunto']
	verbose_name = "Asunto"
	verbose_name_plural = "Asuntos"

class TemploInline(admin.TabularInline):
	model=Templo.agenda.through
	autocomplete_fields = ['templo']
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