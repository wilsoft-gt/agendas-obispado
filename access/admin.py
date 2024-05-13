from django.contrib import admin
from .models import AuthToken

# Register your models here.
class AuthTokenAdmin(admin.ModelAdmin):
	model=AuthToken
	readonly_fields = ("value",)

admin.site.register(AuthToken, AuthTokenAdmin)