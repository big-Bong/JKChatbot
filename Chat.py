import requests
from flask import Flask, request

from ChatGPTConnect import askgpt

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    print(request.json)
    query = request.json["query"]
    answer = askgpt(query)
    return str(answer)

if __name__ == '__main__':
    app.run(port=4000)