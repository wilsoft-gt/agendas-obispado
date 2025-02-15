"""whatsapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from api.views import render_agenda, agenda_pdf, home, discursante_pdf, oracion_pdf
from access.views import EndPointViewset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:pk>/', render_agenda, name="agenda"),
    path('agenda-pdf/<int:pk>/', agenda_pdf, name="descargaPDF"),
    path('discurso/<int:pk>/', discursante_pdf, name="discurso"),
    path('oracion/<int:pk>/', oracion_pdf, name="oracion"),
    path('', home, name="home"),
    path('api/V1.0/wa/webhoook/', EndPointViewset.as_view(), name="webhook"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
