import requests
import sqlite3 as sq
from enum import Enum


class Status(Enum):
    Added = 0
    Updated = 1


class Bot:
    def __init__(self, token: str, port: str):
        self.__token = token
        self.__port = port

    @staticmethod
    def __add_user(chat_id: int, eth_address: str) -> Status:
        with sq.connect('bridge.db') as con:
            cur = con.cursor()
            result = cur.execute('SELECT id FROM users WHERE chat_id = ?', (chat_id,)).fetchone()

            if result is None:
                cur.execute('INSERT INTO users (chat_id, eth_address) VALUES (?, ?)', (chat_id, eth_address))
                return Status.Added

            else:
                cur.execute('UPDATE users SET eth_address = ? WHERE id = ?', (eth_address, result[0]))
                return Status.Updated

    def __api_request(self, method: str, data: dict):
        url = f'https://api.telegram.org/bot{self.__token}/{method}'
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        requests.post(url, headers=headers, json=data)

    def send_message(self, chat_id: str, text: str):
        data = {"chat_id": chat_id, "text": text}
        self.__api_request('sendMessage', data)

    def handle_request(self, request: dict):
        chat_id = request['message']['chat']['id']
        message_text = request['message']['text']
        command = message_text.split()
        text = 'Incorrect command'

        if len(command) == 2 and command[0] == '/add':
            status = self.__add_user(chat_id, command[1])

            if status == Status.Added:
                text = 'Address was successfully added'

            elif status == Status.Updated:
                text = 'Address was successfully updated'

        self.send_message(chat_id, text)
