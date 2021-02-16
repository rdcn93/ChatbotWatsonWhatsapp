from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json

app = Flask(__name__)

@app.route("/bot", methods=['GET', 'POST'])
def bot():
    # ibm-watson autenticacion
    authenticator = IAMAuthenticator('2yc97zPkBEuQyq0LENgZn2x6-IpD29Dz-YFZfT2MjogI')

    # anterior 2018-07-10
    assistant = AssistantV2(version='2020-04-01', authenticator=authenticator)

    # Agregar url segun la zona
    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')

    # obtener mensaje enviado desde la llamada al servicio
    msg = request.form.get('Body')

    # validar que se envien los parametros
    if request.form.get('Body') is not None:
        msg = request.form.get('Body')
    elif request.form is not None:
        msg = request.form
    else:
        msg = ''

    # enviar el mensaje a Watson
    response = assistant.message_stateless(
        assistant_id='2c1a74b6-3869-4b09-8e09-133a2d68fd26',
        input={
            'message_type': 'text',
            'text': str(msg)
        }
    ).get_result()

    while True:
        if response['output']['intents']:
            print('Detected intent: #' + response['output']['intents'][0]['intent'])

        # print the output from dialog, if any.
        if response['output']['generic']:
            resp = MessagingResponse()

            for res in response['output']['generic']:
                tipoResultado = res['response_type']

                if tipoResultado == 'text':
                    resp.message(str(res['text']))
                elif tipoResultado == 'image':
                    urlImagen = res['source']
                    tituloImagen = res['title']
                    resp.message(str(tituloImagen)).media(urlImagen)

            return str(resp)
        else:
            sda = ''
            #return str('')

app.run(debug=True)
