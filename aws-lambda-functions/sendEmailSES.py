import json
import boto3
from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):
    
    print("Event details : ",event)
  
    # Obtener variables digitadas por el usuario en el chatbot
    email = event["sessionState"]["intent"]["slots"]["correo"]["value"]["originalValue"]
    direccion = event["sessionState"]["intent"]["slots"]["direccion"]["value"]["originalValue"]
    ciudad = event["sessionState"]["intent"]["slots"]["ciudad"]["value"]["originalValue"]
    departamento = event["sessionState"]["intent"]["slots"]["departamento"]["value"]["originalValue"]
    cupo = event["sessionState"]["intent"]["slots"]["cupo"]["value"]["originalValue"]
    
    print("Email chatbot : ",email)
    print("Direccion chatbot : ",direccion)
    print("Ciudad chatbot : ",ciudad)
    print("Depto chatbot : ",departamento)
    print("Cupo chatbot : ",cupo)
    
    # Obtener datos del cliente desde la DB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('ClientesBBVA')
    result = table.query(
        KeyConditionExpression=Key('email').eq(email)
    )
    #data = client.get_item(TableName='ClientesBBVA',Key={'email': {'S': email}})
    
    print("Datos DB: ", result)
    
    nombre = result["Items"][0]["nombres"]
    apellido = result["Items"][0]["apellidos"]
    
    print("Nombre DB: ",nombre)
    print("Apellido DB : ",apellido)
    
    # Envío de correo
    
    subject = 'BBVA - Detalles del contrato tarjeta Aqua'
    client = boto3.client("ses")
    body = """
                 Hola {} {}, nos alegra que aceptaras tu tarjeta de crédito Aqua BBVA.
                 <br><br>
                 Dicha tarjeta te fue aprobada con un cupo de ${} pesos colombianos. 
                 <br>
                 La dirección de envío a la cual llegará tu tarjeta es {} ubicada en la ciudad de {} en el departamento de {}.
                 <br><br>
                 Si tienes dudas por favor <a href="https://www.bbva.com.co/personas/lineas-de-atencion.html">ingresa aquí</a> para contactarnos.
                 <br>
                 Un saludo de tus amigos de BBVA Colombia.
         """.format(nombre, apellido, cupo, direccion, ciudad, departamento)
    message = {"Subject": {"Data": subject}, "Body": {"Html": {"Data": body}}}
    response = client.send_email(Source = "davidrojas0030@gmail.com", Destination = {"ToAddresses": [email]}, Message = message) 
    print("The mail is sent successfully")