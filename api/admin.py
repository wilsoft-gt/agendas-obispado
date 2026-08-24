from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.html import format_html
from django.db.models import OuterRef, Subquery
from .models import Obispado, Organizacion, Templo, Limpieza, Asunto, Actividad, Agenda, Himno, Oracion, Discurso, Miembro
from datetime import date, datetime
# Register your models here.

admin.site.site_header = "Barrio Pinares 1"
admin.site.site_title = "Barrio Pianres 1"


class FiftyPerPageAdmin(admin.ModelAdmin):
	list_per_page = 50


admin.site.register(Obispado, FiftyPerPageAdmin)
admin.site.register(Organizacion, FiftyPerPageAdmin)


class AsuntoAdmin(FiftyPerPageAdmin):
	search_fields = ['titulo', 'descripcion', 'organizacion__nombre']
	

admin.site.register(Asunto, AsuntoAdmin)


class TemploAdmin(FiftyPerPageAdmin):
	search_fields = ['observaciones', 'reservado_por__nombre']


admin.site.register(Templo, TemploAdmin)


class ActividadAdmin(FiftyPerPageAdmin):
	search_fields = ['titulo', 'lugar', 'organizacion__nombre']


admin.site.register(Actividad, ActividadAdmin)



def calcular_fechas(fecha):
	if isinstance(fecha, datetime):
		fecha = fecha.date()
	hoy = date.today()
	futura = fecha > hoy
	fecha_comparacion = fecha if futura else hoy
	hoy_comparacion = hoy if futura else fecha

	def expresar(valor, singular, plural):
		texto = singular if valor == 1 else plural
		return f'{valor} {texto}'

	def prefijo(texto):
		return f'En {texto}' if futura else f'Hace {texto}'

	años = fecha_comparacion.year - hoy_comparacion.year
	try:
		aniversario = hoy_comparacion.replace(year=fecha_comparacion.year)
	except ValueError:
		aniversario = hoy_comparacion.replace(year=fecha_comparacion.year, day=28)
	if aniversario > fecha_comparacion:
		años -= 1
	if años:
		return prefijo(expresar(años, 'año', 'años'))

	meses = ((fecha_comparacion.year - hoy_comparacion.year) * 12
			 + fecha_comparacion.month - hoy_comparacion.month)
	if fecha_comparacion.day < hoy_comparacion.day:
		meses -= 1
	if meses:
		return prefijo(expresar(meses, 'mes', 'meses'))

	dias = abs((hoy - fecha).days)
	semanas = dias // 7
	if semanas:
		return prefijo(expresar(semanas, 'semana', 'semanas'))
	return prefijo(expresar(dias, 'día', 'días'))


class MiembroAdmin(FiftyPerPageAdmin):
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
			return format_html(f'<span>{calcular_fechas(fecha)} ({fecha})</span>')
		return format_html('<span>No ha discursado</span>')

	def ultimoDiscursoTema(self, obj):
		tema = getattr(obj, 'ultimo_discurso_tema', None)
		if tema:
			return format_html(f'<span>{tema}</span>')
		return format_html('<span>Sin datos</span>')
	
	def ultimaOracion(self, obj):
		fecha = getattr(obj, 'ultima_oracion_fecha', None)
		if fecha:
			return format_html(f'<span>{calcular_fechas(fecha)} ({fecha})</span>')
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


class AgendaAdmin(FiftyPerPageAdmin): 
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