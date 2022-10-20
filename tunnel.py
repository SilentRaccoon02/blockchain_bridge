import logging
import requests
import subprocess

log = logging.getLogger(__name__)


class Tunnel:
    def __init__(self, token: str, port: str):
        self.__ngrok = None
        self.__public_url = None
        self.__token = token
        self.__port = port

    def __run_ngrok(self):
        self.__ngrok = subprocess.Popen(['ngrok', 'http', self.__port])
        localhost_url = 'http://localhost:4040/api/tunnels'
        tunnel_info = requests.get(localhost_url).json()
        public_url = tunnel_info['tunnels'][0]['public_url']
        self.__public_url = public_url
        log.info(f'ngrok public ulr: {public_url}')

    def __webhook(self, action: str):
        method = 'setWebhook'
        data = {'url': self.__public_url if action == 'set' else ''}
        url = f'https://api.telegram.org/bot{self.__token}/{method}'
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        response = requests.post(url, headers=headers, json=data)
        log.info(f'response description: {response.json()["description"]}')

    def open(self):
        self.__run_ngrok()
        self.__webhook('set')

    def close(self):
        self.__webhook('delete')
        self.__ngrok.kill()

    def __del__(self):
        self.close()
