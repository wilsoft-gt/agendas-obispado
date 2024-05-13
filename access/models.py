from django.db import models
from django.utils.crypto import get_random_string

# Create your models here.

class AuthToken(models.Model):
	app = models.CharField(max_length=20)
	key = models.CharField(max_length=20)
	value = models.CharField(max_length=32)
	def save(self, *args, **kwargs):
		self.value = get_random_string(length=32)
		super(AuthToken, self).save(*args, **kwargs)


	def __str__(self):
		return self.app