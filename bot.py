from ibm_watson import AssistantV1
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
    
    #anterior 2018-07-10
    assistant = AssistantV1(version='2020-04-01', authenticator=authenticator)

    # Agregar url segun la zona
    assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')

    responseLW=assistant.list_workspaces().get_result()

    print(responseLW)

    # check workspace status (wait for training to complete)
    workspace_id = '350afcf8-f545-46a6-a88c-1e98a88eae0c'
    workspace = assistant.get_workspace(workspace_id=workspace_id).get_result()

    print('The workspace status is: {0}'.format(workspace['status']))

    if workspace['status'] == 'Available':
        print('Ready to chat!')
    else:
        print('The workspace should be available shortly. Please try again in 30s.')
        print('(You can send messages, but not all functionality will be supported yet.)')

    # responde to inscoming calls with a simple text message
    # fetch the message
    msg = request.form.get('Body')

    input = {'text': msg}
    response = assistant.message(
        workspace_id=workspace_id, input=input).get_result()
    print(json.dumps(response, indent=2))

    while True:
        if response['intents']:
            print('Detected intent: #' + response['intents'][0]['intent'])

        # print the output from dialog, if any.
        if response['output']['text']:
            resp = MessagingResponse()
            resp.message(str(response['output']['text'][0]))
            return str(resp)


app.run(debug=True)
