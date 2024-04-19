from django.db import models
from .opciones import LLAMAMIENTOS, LISTA_HIMNOS, TIPO_HIMNO, TIPO_ORACION

# Create your models here.

class Obispado(models.Model):
	nombre = models.CharField(max_length=50)
	llamamiento = models.CharField(choices=LLAMAMIENTOS, max_length=2)
	class Meta(object):
		verbose_name_plural = "Obispado"
	def __str__(self):
		return f"{LLAMAMIENTOS[self.llamamiento]} - {self.nombre}"
	

class Organizacion(models.Model):
	nombre = models.CharField(max_length=50)
	codigo = models.CharField(max_length=15)
	class Meta(object):
		verbose_name_plural = "Organizaciones"
	
	def __str__(self):
		return self.nombre
	

class Agenda(models.Model):
	fecha = models.DateField(auto_now=False, auto_now_add=False)
	primer_domingo = models.BooleanField(default=False)
	dirige = models.ForeignKey(Obispado, models.SET_NULL, blank=True, null=True, related_name="dirige")
	preside = models.ForeignKey(Obispado, models.SET_NULL, blank=True, null=True, related_name="preside")
	piano = models.CharField(max_length=50, default="Jose Galicia")
	direccion_himnos = models.CharField(max_length=50, default="Alma Aceituno")
	def __str__(self):
		return str(self.fecha)

class Templo(models.Model):
	fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
	reservado_por = models.ForeignKey(Obispado, models.SET_NULL, blank=True, null=True)
	reserva_confirmada = models.BooleanField(default=False)
	observaciones = models.TextField(blank=True)
	agenda = models.ManyToManyField(Agenda, blank=True)

	class Meta(object):
		verbose_name_plural = "Templo"

	def __str__(self):
		return str(self.fecha.strftime("%d/%m/%Y - %I:%M%p"))

class Entrevista(models.Model):
	nombre = models.CharField(max_length=50)
	fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
	quien_realiza = models.ForeignKey(Obispado, models.SET_NULL, blank=True, null=True)
	def __str__(self):
		return self.nombre

class Himno(models.Model):
	numero = models.CharField(choices=LISTA_HIMNOS, max_length=50)
	tipo = models.CharField(choices=TIPO_HIMNO, max_length=3)
	agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return self.numero

class Limpieza(models.Model):
	fecha = models.DateField(auto_now=False, auto_now_add=False)
	organizacion = models.ForeignKey(Organizacion, models.SET_NULL, blank=False, null=True)
	finalizada = models.BooleanField()
	agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, blank=True, null=True)
	class Meta(object):
		verbose_name_plural = "Limpieza"
	
	def __str__(self):
		return f"{self.fecha.strftime('%d/%m/%Y')} - {self.organizacion}"

class Oracion(models.Model):
	nombre = models.CharField(max_length=50)
	tipo = models.CharField(choices=TIPO_ORACION, max_length=10)
	confirmado = models.BooleanField(default=False)
	agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, blank=True, null=True)
	def __str__(self):
		return f"{self.agenda} - {self.nombre}"
	

class Asunto(models.Model):
	organizacion = models.ForeignKey(Organizacion, models.SET_NULL, blank=True, null=True)
	titulo = models.CharField(max_length=50)
	descripcion = models.TextField(blank=True)
	fecha = models.DateField(auto_now=False, auto_now_add=False)
	encargado = models.ForeignKey(Obispado, models.SET_NULL, blank=True, null=True)
	agenda = models.ManyToManyField(Agenda, blank=True)
	def __str__(self):
		return	f"{self.titulo} - {self.organizacion}"

class Actividad(models.Model):
	organizacion = models.ForeignKey(Organizacion, models.SET_NULL, blank=False, null=True)
	titulo = models.CharField(max_length=50)
	descripcion = models.TextField()
	fecha = models.DateTimeField(auto_now=False, auto_now_add=False)
	presupuesto = models.BooleanField(default=False)
	aprobado = models.BooleanField(default=False)
	agenda = models.ManyToManyField(Agenda, blank=True)
	class Meta(object):
		verbose_name_plural = "Actividades"
	def __str__(self):
		return	f"{self.titulo} - {self.organizacion}"

class Discursante(models.Model):
	nombre = models.CharField(max_length=50)
	tema = models.CharField(max_length=50)
	cofirmado = models.BooleanField(default=False)
	agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE, blank=True, null=True)
	def __str__(self):
		return	f"{self.nombre} - {self.tema}"