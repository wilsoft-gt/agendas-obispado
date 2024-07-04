from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
from .permissions import AccessTokenPermission
from .models import AuthToken
from .whatsapp import WhatsappHandler, proximo_domingo
from api.models import Discursante, Oracion

allowed_actions = ["discur", "oraci"]

class EndPointViewset(APIView):
    permission_classes = [AccessTokenPermission]
    handler = None
    def post(self, request):
        if "messages" in request.data["entry"][0]["changes"][0]["value"].keys():
            handler = WhatsappHandler(request.data)
            
            if (handler.get_type() == "text") and any(sub in handler.get_text_body() for sub in allowed_actions):
                if ("discur" in handler.get_text_body()):
                    self.handle_discursante(handler)
                elif ("oraci" in handler.get_text_body()):
                    self.handle_oraciones(handler)

            elif (handler.get_type() == "interactive"):
                if (handler.get_interactive_button_id() == "discursantes_button"):
                    handler.return_reaction()
                    self.handle_discursante(handler)
                elif (handler.get_interactive_button_id() == "oraciones_button"):
                    handler.return_reaction()
                    self.handle_oraciones(handler)
                elif (handler.get_interactive_button_id() == "agendas_button"):
                    handler.return_reaction()
                    handler.return_text_message("Link de las agendas: \nhttps://wilsoft.pythonanywhere.com/admin/api/agenda/")
            else:
                handler.return_main_menu()

            return HttpResponse(status=200)
        else:
            print("Mensaje generico de whatsapp api recibido!")
            return HttpResponse(status=204)

    def get(self, request):
        access_token = AuthToken.objects.filter(value=request.query_params["hub.verify_token"]).exists()
        if(request.query_params["hub.mode"] == "subscribe" and access_token):
            return HttpResponse(request.query_params['hub.challenge'], status=200)
        else:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)
        
    def handle_discursante(self, handler):
        discursantes = Discursante.objects.filter(agenda__fecha=proximo_domingo())
        if discursantes:
            dis_lista = [f"\n{dis.nombre} - _{dis.tema}_" for dis in discursantes]
            body = f"*Lista de discursantes para el domingo {proximo_domingo().strftime('%d/%m/%Y')}:* {''.join(dis_lista)}"
        else:
            body = f"No hay discursantes registrados para el domingo {proximo_domingo().strftime('%d/%m/%Y')}. \n Puedes ver las agendas siguiendo el siguiente link:\n https://wilsoft.pythonanywhere.com/admin/api/agenda/"
        handler.return_reaction()
        handler.return_text_message(body)

    def handle_oraciones(self, handler):
        oraciones = Oracion.objects.filter(agenda__fecha=proximo_domingo())
        if oraciones:
            ora_lista = [f"\n{ora.nombre} - _{ora.tipo}_" for ora in oraciones]
            body = f"*Lista de oraciones para el domingo {proximo_domingo().strftime('%d/%m/%Y')}:* {''.join(ora_lista)}"
        else:
            body = f"No hay oraciones registradas para el domingo {proximo_domingo().strftime('%d/%m/%Y')} \n Puedes ver las agendas siguiendo el siguiente link:\n https://wilsoft.pythonanywhere.com/admin/api/agenda/"
        handler.return_reaction()
        handler.return_text_message(body)