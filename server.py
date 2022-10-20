import json
from flask import Flask, request
from bot import Bot

app = Flask(__name__)

with open('config.json') as file:
    config = json.load(file)
    token = config['bot']['token']
    port = config['bot']['port']


@app.route('/', methods=['POST'])
def receive_update() -> dict:
    if request.method == 'POST':
        bot = Bot(token, port)
        bot.handle_request(request.json)
    return {'ok': True}


if __name__ == '__main__':
    app.run()
