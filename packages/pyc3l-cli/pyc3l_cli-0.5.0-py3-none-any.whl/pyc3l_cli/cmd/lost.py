#!/usr/bin/env python


import click
import sys
import time
import getpass

from pyc3l import Pyc3l
from pyc3l_cli import common


from urllib.request import urlopen
import json


class Report:
    def __init__(self, currency):
        self.currency = currency
        self.error_info = []
        self.wallet_list = []

    def addErrors(self, address, errors_info):
        self.wallet_list.append(address)
        self.error_info.extend(errors_info)

    def printReport(self):
        print("Monnaie : " + self.currency)
        print("Nombre de comptes : " + str(len(self.wallet_list)))
        print("Nombre d'erreur/transactions pending : " + str(len(self.error_info)))

    def impactedWallet(self):
        w_list = {}
        for error in self.error_info:
            ad1 = error["add1"]
            if ad1 not in w_list:
                w_list[ad1] = 0
            w_list[ad1] += 1
            ad2 = error["add2"]
            if ad2 not in w_list:
                w_list[ad2] = 0
            w_list[ad2] += 1

        w_list = dict(sorted(w_list.items(), key=lambda x: x[1], reverse=True))

        for ad in w_list:
            if ad != "Admin":
                print(
                    f"Le compte {ad} participe à {w_list[ad]} transaction pending ou échouées."
                )
            else:
                print(f"{w_list[ad]} opérations de crédits sont pending ou échouées.")


def read_data(file):
    """Returns iterator of 2-uple (currency, address) from rows of file

    The values are separated by a comma.

    """
    with open(file, "r") as f:
        for line in f:
            currency, address = line.strip().split(",")
            yield currency.strip(), address.strip()


## Get the total number of lines in a file
def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1


## Read lines from file

total = file_len(filename)
print(f" Nombre total de comptes: {total}")

BASE_URL = "https://node-cc-001.cchosting.org/lost_trn.php?addr="


def fetch_pending_and_rejected(address):
    content = urlopen(BASE_URL + address).read()
    data = json.loads(content)
    return data["pending_and_rejected"]


reports = {}
error_address = []
for idx, (currency, address) in enumerate(read_data(filename)):
    report = reports.get(currency, Report(currency))
    try:
        pending_and_rejected = fetch_pending_and_rejected(address)
        report.addErrors(address, pending_and_rejected)
    except:
        print(
            f"Erreur lors de la récupération des transactions pour {address} sur la monnaie {currency}"
        )
        error_address.append(address)

    if idx % 100 == 0:
        print(f"{int(100 * idx / total)}% processé...")

print(f"Nombre de comptes sans réponses : {len(error_address)}")
print(error_address)

for report in reports.values():
    report.printReport()
    report.impactedWallet()


@click.command()
@click.option("-w", "--wallet-file", help="wallet path")
@click.option("-p", "--password-file", help="wallet password path")
@click.option("-d", "--csv-data-file", help="CSV data path")
@click.option("-D", "--delay", help="delay between blockchain request", default=15)
@click.option("-e", "--endpoint", help="Force com-chain endpoint.")
@click.option("-W", "--wait", help="wait for integration in blockchain", is_flag=True)
@click.option(
    "-y",
    "--no-confirm",
    help="Bypass confirmation and always assume 'yes'",
    is_flag=True,
)
def run(wallet_file, password_file, csv_data_file, delay, endpoint, wait, no_confirm):
    """Batch pledging using CSV file"""

    ################################################################################
    ##     (1) CSV file handling
    ################################################################################
    csv_data_file = csv_data_file or common.filepicker("Choose a CSV file")
    transactions = list(
        map(
            lambda record: {
                "address": record["Address"],
                "amount": float(record["Montant"]),
                "message": record["Message"],
            },
            common.readCSV(csv_data_file),
        )
    )

    print(f"The file {csv_data_file!r} has been read.")
    print(
        "It contains %s transaction(s) for a total of %s"
        % (
            len(transactions),
            sum(t["amount"] for t in transactions),
        )
    )

    if not no_confirm and not input("Continue to the execution (y/n)") == "y":
        sys.exit()

    ################################################################################
    ##     (2) Load the account and check funds availability
    ################################################################################

    # Load the API
    print("INFO: Load the API.")
    pyc3l = Pyc3l(endpoint)

    wallet = pyc3l.Wallet.from_file(
        wallet_file or common.filepicker("Select Admin Wallet")
    )

    wallet.unlock(
        common.load_password(password_file) if password_file else getpass.getpass()
    )

    print("INFO: Check the provided account to have admin role.")
    if not wallet.IsValidAdmin:
        print("Error: The wallet's account is not admin")
        sys.exit(1)

    if not wallet.isActive:
        print("Error: The Admin Wallet is locked!")
        sys.exit(1)

    ################################################################################
    ##     (3) Check target accounts are available
    ################################################################################

    currency = wallet.currency
    transactions = map(
        lambda t: dict(t, unlocked=currency.Account(t["address"]).isActive),
        transactions,
    )

    if (
        not no_confirm
        and not input(f"Ready to pledge some {wallet['server']['name']} ? (y/n) ")
        == "y"
    ):
        sys.exit()

    ################################################################################
    ##     (4) Execute transactions
    ################################################################################
    transaction_hash = {}
    for t in transactions:
        if not t["unlocked"]:
            print(f"Transaction to {t['address']} skipped")
            continue

        res = wallet.pledge(t["address"], t["amount"], message_to=t["message"])
        transaction_hash[res] = t["address"]
        print(
            "Transaction Nant sent to %s (%.2f LEM) with message %r Transaction Hash=%s"
            % (
                t["address"],
                t["amount"],
                t["message"],
                res,
            )
        )

        time.sleep(delay)  # Delay for not overloading the BlockChain

    print("All transaction have been sent!")

    if wait:
        common.wait_for_transactions(pyc3l, transaction_hash)


if __name__ == "__main__":
    run()
