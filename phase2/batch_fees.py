from requests import get
from sys import exit
UMEE_ERC20 = "0xe54fbaecc50731afe54924c40dfd1274f718fe02"
NODE_URL = "http://localhost:1317/"
FAKE_API = f"https://peggo-fakex-qhcqt.ondigitalocean.app/"\
          f"api/v3/simple/token_price/ethereum?"\
          f"contract_addresses={UMEE_ERC20}&vs_currencies=usd"


def get_price():

    try:
        response = get(FAKE_API).json()
        for addr, price in response.items():
            return price['usd']
    except Exception as err:
        print(f"[ERR] {err}")
        exit(0)


def get_batches():
    url = f"{NODE_URL}/peggy/v1/batch/outgoingtx"

    try:
        response = get(url).json()
        return response
    except Exception as err:
        print(f"[ERR] {err}")
        exit(0)


def get_fee():

    batches = get_batches()
    nonce_and_fees = dict()
    try:
        for batch in batches['batches']:
            nonce_and_fees[batch['batch_nonce']] = 0

            for tx in batch['transactions']:
                nonce_and_fees[batch['batch_nonce']] += int(tx['erc20_fee']['amount']) / 1000000

        return dict(sorted(nonce_and_fees.items()))

    except Exception as err:
        print(f'[ERR] {err}')
        exit(0)


def main():
    fees = get_fee()
    price = get_price()

    for nonce, fee in fees.items():
        print(f"nonce: {nonce} fees: {fee*price:.1f}$")


if __name__ == '__main__':
    main()
