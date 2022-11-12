from solana.rpc.api import Client, Keypair, PublicKey, Transaction
from solana.transaction import AccountMeta, TransactionInstruction
from solana.system_program import SYS_PROGRAM_ID

import json


def main():
    http_client = Client('http://127.0.0.1:8899')

    with open('solana/wallet.json') as file:
        data = json.load(file)
        wallet_keypair = Keypair().from_secret_key(data)

    with open('solana/test.json') as file:
        data = json.load(file)
        test_keypair = Keypair().from_secret_key(data)

    with open('solana/contract.json') as file:
        data = json.load(file)
        contract_keypair = Keypair().from_secret_key(data)

    ix = TransactionInstruction(
        [AccountMeta(wallet_keypair.public_key, True, True),
         AccountMeta(test_keypair.public_key, False, True),
         AccountMeta(SYS_PROGRAM_ID, False, False)],
        contract_keypair.public_key,
        (500000000).to_bytes(8, 'little')
    )

    txn = Transaction().add(ix)
    result = http_client.send_transaction(txn, wallet_keypair)
    print(result)

    # http_client.confirm_transaction(res.value)


if __name__ == '__main__':
    main()
