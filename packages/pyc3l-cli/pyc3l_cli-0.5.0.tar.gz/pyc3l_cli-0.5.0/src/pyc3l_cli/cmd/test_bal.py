#!/usr/bin/env python

import datetime
import click
from web3 import Web3

from pyc3l import Pyc3l, ApiHandling
from pyc3l_cli import common

@click.command()
@click.option("-e", "--endpoint", help="Force com-chain endpoint.")
@click.option("-r", "--raw", is_flag=True, help="Print raw values.")
@click.argument("currency")
@click.argument("address")
def run(endpoint, currency, address, raw):
    print(f"{'Endpoint':<13} {'gasPrice':>9} {'Balance':>10}")
    print("-" * 38)
    endpoints = ApiHandling().endpoints
    for endpoint in sorted(endpoints, key=lambda e: str(e)):

        pyc3l = Pyc3l(str(endpoint))

        cur = pyc3l.Currency(currency)
        account = cur.Account(address)
        endpoint_short = str(endpoint).split("/", 3)[2]
        endpoint_short = endpoint_short.split(".", 1)[0]
        tr_infos = pyc3l.getTrInfos("0x" + "0" * 40)
        gas_price = Web3.fromWei(int(tr_infos['gasprice'], 16), 'gwei')
        print(f"{endpoint_short:<13} {gas_price:4} gwei {account.globalBalance:8.2f} {cur.symbol}")
        # print(f"  ETH balance = {account.eth_balance_wei} Wei (={account.eth_balance} Ether)")


if __name__ == "__main__":
    run()
