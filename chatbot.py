from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from flask import Flask, request, redirect
from twilio.twiml.messaging_response import MessagingResponse
import requests
import json

app = Flask(__name__)

@app.route("/bot", methods=['GET', 'POST'])
def bot():
    # ibm-watson auth
    authenticator = IAMAuthenticator('2yc97zPkBEuQyq0LENgZn2x6-IpD29Dz-YFZfT2MjogI')

    # anterior 2018-07-10
    assistant = AssistantV2(version='2020-04-01', authenticator=authenticator)

    # Agregar url segun la zona
    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')

    # responde to inscoming calls with a simple text message
    # fetch the message
    msg = request.form.get('Body')

    if request.form.get('Body') is not None:
        msg = request.form.get('Body')
    elif request.form is not None:
        msg = request.form
    else:
        msg = ''

    input = {'text': msg}

    # response = assistant.message(
    #     workspace_id=workspace_id, input=input).get_result()

    # responseSesId = assistant.create_session(assistant_id='2c1a74b6-3869-4b09-8e09-133a2d68fd26').get_result()

    # response = assistant.message(
    #     assistant_id='2c1a74b6-3869-4b09-8e09-133a2d68fd26',
    #     session_id= str(responseSesId),
    #     input={
    #         'message_type': 'text',
    #         'text': str(input)
    #     }
    # ).get_result()

    response = assistant.message_stateless(
        assistant_id='2c1a74b6-3869-4b09-8e09-133a2d68fd26',
        input={
            'message_type': 'text',
            'text': str(msg)
        }
    ).get_result()

    # response = assistant.delete_session(assistant_id='2c1a74b6-3869-4b09-8e09-133a2d68fd26',session_id=str(responseSesId)).get_result()
    # print(json.dumps(response, indent=2))

    while True:
        if response['output']['intents']:
            print('Detected intent: #' + response['output']['intents'][0]['intent'])

        # print the output from dialog, if any.
        if response['output']['generic']:
            resp = MessagingResponse()

            tipoResultado = response['output']['generic'][0]['response_type']

            if tipoResultado == 'text':
                resp.message(str(response['output']['generic'][0]['text']))
            elif tipoResultado == 'image':
                urlImagen = response['output']['generic'][0]['source']
                tituloImagen = response['output']['generic'][0]['title']
                resp.message(str(tituloImagen)).media(urlImagen)
                        
            return str(resp)


app.run(debug=True)
