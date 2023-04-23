import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

from ChatGPTConnect import askgpt

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    print(request.json)
    query = request.json["query"]
    resp = MessagingResponse()
    msg = resp.message()
    answer, log = askgpt(query)
    msg.body(answer)
    return str(resp)

if __name__ == '__main__':
    app.run(port=4000)
"""
query = ""
while(query!="thank you"):
    query = input("User: ")
    answer, log = askgpt(query)
    print("Bot: "+answer+"\n")
"""
