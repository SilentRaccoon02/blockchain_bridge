from solana.rpc.api import Client, Keypair, PublicKey, Transaction
from solana.transaction import AccountMeta, TransactionInstruction
from solana.system_program import SYS_PROGRAM_ID

import json
import logging
import os

log = logging.getLogger(__name__)


class Solana:
    def __init__(self, contract_path: str, wallet_path: str, test_path: str, port: str):
        self.__contract_keypair = None
        self.__wallet_keypair = None
        self.__test_keypair = None
        self.__client = None
        self.__contract_path = contract_path
        self.__wallet_path = wallet_path
        self.__test_path = test_path
        self.__port = port

    def connect(self):
        url = f'http://127.0.0.1:{self.__port}'
        self.__client = Client(url)

        with open(os.getcwd() + self.__contract_path) as file:
            data = json.load(file)
            self.__contract_keypair = Keypair().from_secret_key(data)

        with open(os.getcwd() + self.__wallet_path) as file:
            data = json.load(file)
            self.__wallet_keypair = Keypair().from_secret_key(data)

        with open(os.getcwd() + self.__test_path) as file:
            data = json.load(file)
            self.__test_keypair = Keypair().from_secret_key(data)
            log.info(f'solana test address: {self.__test_keypair.public_key}')
            log.info(f'solana test amount: 500000000')

    def transaction(self, address: str, amount: int):
        to = PublicKey(address)

        ix = TransactionInstruction(
            [AccountMeta(self.__wallet_keypair.public_key, True, True),
             AccountMeta(to, False, True),
             AccountMeta(SYS_PROGRAM_ID, False, False)],
            self.__contract_keypair.public_key,
            amount.to_bytes(8, 'little')
        )

        txn = Transaction().add(ix)
        result = self.__client.send_transaction(txn, self.__wallet_keypair)
        log.info(f'transaction completed {result.value}')
