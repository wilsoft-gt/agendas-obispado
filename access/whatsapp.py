import environ
import urllib3
import json
import os
from datetime import datetime, timedelta
from django.http import HttpResponse
from dataclasses import dataclass
from django.conf import settings

env = environ.Env()
environ.Env.read_env(os.path.join(settings.BASE_DIR, ".env"))

def proximo_domingo(): 
   today = datetime.today()
   days_until_sunday = (6 - today.weekday()) % 7
   next_sunday = today + timedelta(days=days_until_sunday)
   return next_sunday

def interactive_main_menu_response(phone_number):
  return {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": f"{phone_number}",
  "type": "interactive",
  "interactive": {
    "type": "button",
    "header": {
        "type": "text",
        "text": "Menu principal"
    },
    "body": {
      "text": "Selecciona una de las opciones. O puedes obtener los datos del domingo siguiente escribiendo: \ndiscursantes\noraciones"
    },
    "footer": {
      "text": "Desarrollado por Wilson Romero (V1.0b)"
    },
    "action": {
      "buttons": [
        {
          "type": "reply",
          "reply": {
              "id": "discursantes_button",
              "title": "Discursantes"
          }
        },
        {
          "type": "reply",
          "reply": {
            "id": "oraciones_button",
            "title": "Oraciones"
          }
        },
        {
          "type": "reply",
          "reply": {
            "id": "agendas_button",
            "title": "Link de Agendas"
          }
        }
      ]
    }
  }
}

def text_response(phone_number, body):
   return {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": f"{phone_number}",
  "type": "text",
  "text": {
    "preview_url": True,
    "body": f"{body}"
  }
}

def reaction_response(phone_number, message_id, emoji):
   return {
  "messaging_product": "whatsapp",
  "recipient_type": "individual",
  "to": f"{phone_number}",
  "type": "reaction",
  "reaction": {
    "message_id": f"{message_id}",
    "emoji": f"{emoji}"
  }
}

@dataclass
class WhatsappHandler:
    data: object  

    def get_type(self):
       return self.data["entry"][0]["changes"][0]["value"]["messages"][0]["type"]
    
    def get_phone_number(self):
       return self.data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
    
    def get_text_body(self):
       return self.data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"].lower()
    
    def get_interactive_button_id(self):
       return self.data["entry"][0]["changes"][0]["value"]["messages"][0]["interactive"]["button_reply"]["id"]
    
    def get_message_id(self):
       return self.data["entry"][0]["changes"][0]["value"]["messages"][0]["id"]
    
    def post_handler(self, action_function, *args):
      if settings.DEBUG:
        http = urllib3.PoolManager()
      else:
        http = urllib3.ProxyManager(env('PROXY'))
      headers = {"Content-Type": "application/json", "Authorization": f"Bearer {env('API_AUTH_TOKEN')}"}
      body = json.dumps(action_function(self.get_phone_number(), *args))
      response = http.request("POST", env("API_URL"), headers=headers, body=body)
      return response
       
    def return_main_menu(self):
       res = self.post_handler(interactive_main_menu_response)
       print("Respuesta: ",res.data.decode("utf-8"))
       return HttpResponse(status=200)
    
    def return_text_message(self, text):
       res = self.post_handler(text_response, text)
       print("Respuesta: ",res.data.decode("utf-8"))
       return HttpResponse(status=200)
    
    def return_reaction(self):
       res = self.post_handler(reaction_response, self.get_message_id(), "👍🏼")
       print("Respuesta: ", res.data.decode("utf-8"))
       return HttpResponse(status=200)
