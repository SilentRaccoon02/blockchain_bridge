import json
import os
from typing import Tuple
from web3 import Web3, types


class Ethereum:
    def __init__(self, address: str, path: str, port: str):
        self.__web3 = None
        self.__contract = None
        self.__address = address
        self.__path = path
        self.__port = port

    def connect(self):
        with open(os.getcwd() + self.__path) as file:
            metadata = json.load(file)
            abi = metadata['output']['abi']

        url = f'http://127.0.0.1:{self.__port}'
        self.__web3 = Web3(Web3.HTTPProvider(url))
        self.__contract = self.__web3.eth.contract(types.ENS(self.__address), abi=abi)

    def read_payments_number(self) -> int:
        result = self.__contract.functions.payments_number().call()
        return result

    def read_payment(self, index: int) -> Tuple:
        result = self.__contract.functions.payments(index).call()
        return result
