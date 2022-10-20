import json
import logging
import time
import sqlite3 as sq
from threading import Thread, Event

from bot import Bot
from ethereum import Ethereum
from tunnel import Tunnel

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


class App:
    def __init__(self, config_path: str):
        self.__close_tunnel = Event()
        self.__quit_loop = Event()
        self.__tunnel_thread = None
        self.__ethereum_thread = None

        with open(config_path) as file:
            self.__config = json.load(file)

        self.__load_bot()
        self.__load_ethereum()

    def __load_bot(self):
        token = self.__config['bot']['token']
        port = self.__config['bot']['port']
        self.__bot = Bot(token, port)

    def __load_ethereum(self):
        port = self.__config['ethereum']['port']
        contract_address = self.__config['ethereum']['contract']['address']
        contract_path = self.__config['ethereum']['contract']['path']
        self.__ethereum = Ethereum(contract_address, contract_path, port)

    def __tunnel(self):
        token = self.__config['bot']['token']
        port = self.__config['bot']['port']

        tunnel = Tunnel(token, port)
        tunnel.open()

        while not self.__close_tunnel.is_set():
            time.sleep(1)

    def __ethereum_loop(self):
        db = self.__config['database']['path']

        while not self.__quit_loop.is_set():
            with sq.connect(db) as con:
                cur = con.cursor()
                last_id = cur.execute('SELECT max(id) FROM payments').fetchone()[0]
                last_id = last_id if last_id is not None else 0
                payments_number = self.__ethereum.read_payments_number()

                for i in range(payments_number - last_id):
                    data = self.__ethereum.read_payment(last_id + i)
                    cur.execute('INSERT INTO payments '
                                '(eth_address, solana_address, amount, status) VALUES (?, ?, ?, ?)', data)

                pending_transactions = cur.execute('SELECT id, eth_address, solana_address, amount '
                                                   'FROM payments WHERE status = 0').fetchall()

                for item in pending_transactions:
                    cur.execute('UPDATE payments SET status = 1 WHERE id = ?', (item[0],))
                    chat_id = cur.execute('SELECT chat_id from users WHERE eth_address LIKE ?', (item[1],)).fetchone()
                    chat_id = chat_id if chat_id is None else chat_id[0]
                    text = f'Transaction detected. Amount: {item[3]}. Solana address: {item[2]}.'
                    self.__bot.send_message(chat_id, text)

            time.sleep(1)

    def __open_tunnel(self):
        log.info('opening tunnel')
        self.__tunnel_thread = Thread(target=self.__tunnel)
        self.__tunnel_thread.start()

    def __connect_ethereum(self):
        log.info('connecting ethereum')
        self.__ethereum.connect()

    def __run_ethereum(self):
        log.info('running ethereum')
        self.__ethereum_thread = Thread(target=self.__ethereum_loop)
        self.__ethereum_thread.start()

    def run(self):
        self.__open_tunnel()
        time.sleep(4)
        self.__connect_ethereum()
        self.__run_ethereum()

    def stop(self):
        log.info('quiting loop')
        self.__quit_loop.set()
        self.__ethereum_thread.join()

        log.info('closing tunnel')
        self.__close_tunnel.set()
        self.__tunnel_thread.join()


if __name__ == '__main__':
    app = App('config.json')
    app.run()

    while True:
        action = input()

        if action == 'stop':
            app.stop()
            break
