from django.urls import path, include
from rest_framework import routers


from .views import EndPointViewset

webhookrouter = routers.DefaultRouter()

webhookrouter.register(r'webhook', EndPointViewset)

urlpatterns = [
    path("/api/V1.0/wa/weebhook", EndPointViewset.as_view(), name="webhook")
]

