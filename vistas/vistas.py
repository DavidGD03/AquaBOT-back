import time
from flask import request
from flask_restful import Resource

from twilio.rest import Client
from boto3 import resource
from vistas import config


AWS_ACCESS_KEY_ID = config.AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY = config.AWS_SECRET_ACCESS_KEY
REGION_NAME = config.REGION_NAME
 
resource = resource(
   'dynamodb',
   aws_access_key_id     = AWS_ACCESS_KEY_ID,
   aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
   region_name           = REGION_NAME
)

class VistaSignIn(Resource):

    def post(self):
        MovieTable = resource.Table('ClientesBBVA')
        response = MovieTable.put_item(
            Item = {
                'email': request.json["email"],
                'nombres' : request.json["nombre"],
                'apellidos' : request.json["apellidos"],
                'sexo' : request.json["sexo"],
                'fecha_nacimiento' : request.json["nacimiento"],
                'fecha_expedicion_cc' : request.json["expedicion"],
                'celular' : request.json["celular"],
                'cedula' : request.json["cedula"],
            }
        )
        global nombres 
        global apellidos 
        
        nombres = request.json["nombre"]
        apellidos = request.json["apellidos"]

        return response



class VistaLogIn(Resource):

    def post(self):
        # Twilio Credentials
        sid='ACc768aba07be273c6004a38d1cacfb0bf'
        authToken='38246239e1d5b431089dbffcd390d988'
        client = Client(sid, authToken)
        # Send whatsapp message
        print('Sending a whatsapp message...')
        message = client.messages.create(to='whatsapp:+' + request.json["celular"], 
                                        from_='whatsapp:+14155238886',
                                        body='Hola ' + nombres + ' '+apellidos+', vimos que no completaste el proceso para obtener tu tarjeta de crédito Aqua BBVA, ¿deseas hacer el proceso por este medio?')
        # Send SMS message
        print('Sending a SMS message...')
        newmessage = client.messages.create(to='+'+ request.json["celular"],  messaging_service_sid='MGdbeb75984a1a004b4dee531150c27f63', 
        body='Hola '+nombres+' '+apellidos+', vimos que no completaste el proceso para obtener tu tarjeta de crédito Aqua BBVA, para continuar da clic en el siguiente link https://api.whatsapp.com/send?phone=+14155238886&text=si%20quiero')
        # Call via voice
        print('Making a call...')
        client.calls.create(to='+'+ request.json["celular"],  from_='+13608002808', method='GET', url='https://aquabot-bucket.s3.amazonaws.com/voice.xml')
        print('Serving TwiML')
        print(request.json["celular"])
        return "Enviando mensajes...", 200