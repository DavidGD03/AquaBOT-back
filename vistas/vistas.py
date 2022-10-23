import time
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from modelos import db, Usuario, UsuarioSchema

from twilio.rest import Client
import datetime
from boto3 import resource
from twilio.twiml.voice_response import VoiceResponse
from vistas import config

usuario_schema = UsuarioSchema()



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
                'nombre' : request.json["nombre"],
                'apellidos' : request.json["apellidos"],
                'sexo' : request.json["sexo"],
                'fecha_nacimiento' : request.json["nacimiento"],
                'fecha_expedicion_cc' : request.json["expedicion"],
                'celular' : request.json["celular"],
                'cedula' : request.json["cedula"],
            }
        )
        return response

    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.contrasena = request.json.get("contrasena", usuario.contrasena)
        db.session.commit()
        return usuario_schema.dump(usuario)

    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204



class VistaLogIn(Resource):

    def post(self):
        sid='ACc768aba07be273c6004a38d1cacfb0bf'
        authToken='38246239e1d5b431089dbffcd390d988'
        client = Client(sid, authToken)

        message = client.messages.create(to='whatsapp:+' + request.json["celular"], 
                                        from_='whatsapp:+14155238886',
                                body='Hola :), vimos que no completaste el proceso para obtener tu tarjeta de crédito Aqua BBVA, ¿deseas hacer el proceso por este medio?')
        
        print('Sending a message...')
        newmessage = client.messages.create(to='+'+ request.json["celular"],  from_='+14155238886', body='Hola :), vimos que no completaste el proceso para obtener tu tarjeta de crédito Aqua BBVA, ¿deseas hacer el proceso por este medio?')

        print('Making a call...')
        newcall = client.calls.create(to='+'+ request.json["celular"],  from_='+14155238886', method='GET')

        print('Serving TwiML')
        twiml_response = VoiceResponse()
        twiml_response.say('Hello!')
        twiml_response.hangup()
        print(request.json["celular"])
        return "Enviando mensaje...", 200

