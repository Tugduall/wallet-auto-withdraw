import time
from web3 import Web3
import requests

infura_url = "https://sepolia.infura.io/v3/<API_TOKEN>"
source_wallet = "<SOURCE_ADDRESS>"
target_wallet = "<TARGET_ADDRESS"
private_key = "<TARGET_PRIVATE_KEY>"

w3 = Web3(Web3.HTTPProvider(infura_url))

if not w3.is_connected():
    raise Exception("Failed to connect to Ethereum network")


def get_eth_usd_price():
    response = requests.get("https://api.coinbase.com/v2/prices/ETH-USD/spot")
    return float(response.json()["data"]["amount"])


def check_and_transfer():
    balance = w3.eth.get_balance(source_wallet)
    balance_eth = w3.from_wei(balance, "ether")

    print("Balance:", balance_eth)

    if balance_eth > 0.001:
        nonce = w3.eth.get_transaction_count(source_wallet)
        gas_price = w3.eth.gas_price
        value = balance - gas_price * 21000

        if value > 0:
            tx = {
                "nonce": nonce,
                "to": target_wallet,
                "value": value,
                "gas": 21000,
                "gasPrice": gas_price,
            }

            signed_tx = w3.eth.account.sign_transaction(tx, private_key)

            tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
            print(f"Transaction sent with hash: {tx_hash.hex()}")


def main():
    while True:
        try:
            check_and_transfer()
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)


if __name__ == "__main__":
    main()
