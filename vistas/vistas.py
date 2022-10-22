import time
from flask import request
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from modelos import db, Usuario, UsuarioSchema

from twilio.rest import Client
import pywhatkit


usuario_schema = UsuarioSchema()



class VistaSignIn(Resource):

    def post(self):
        usuario = Usuario.query.filter(Usuario.usuario == request.json["usuario"]).first()

        if not usuario is None:
            return "Ya existe un usuario con ese nombre.", 404
        else:
            nuevo_usuario = Usuario(usuario=request.json["usuario"], contrasena=request.json["contrasena"], admin=request.json["admin"])
            db.session.add(nuevo_usuario)
            db.session.commit()
            token_de_acceso = create_access_token(identity=nuevo_usuario.id)
            return {"mensaje": "usuario creado exitosamente", "token": token_de_acceso, "id": nuevo_usuario.id}

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

    def get(self):
        pywhatkit.sendwhatmsg("+14155238886", "join world-busy")
        return "Enviando mensaje...", 200


class VistaLogIn(Resource):

    def post(self):
        sid='ACc768aba07be273c6004a38d1cacfb0bf'
        authToken='38246239e1d5b431089dbffcd390d988'
        client = Client(sid, authToken)

        message = client.messages.create(to='whatsapp:+573194625339', 
                                        from_='whatsapp:+14155238886',
                                body='Hola :), vimos que no completaste el proceso para obtener tu tarjeta de crédito Aqua BBVA, ¿deseas hacer el proceso por este medio?')
        return "Enviando mensaje...", 200

