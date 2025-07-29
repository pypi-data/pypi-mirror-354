import click
import re
import getpass

from ..cli import pass_environment


def file_get_contents(filename):
    with open(filename, "r") as f:
        return f.read()


@click.command()
@click.option("-k", "--keyfile", help="key-file path")
@click.option("-p", "--password-file", help="key-file password")
@pass_environment
def run(ctx, keyfile, password_file, *args, **kwargs):
    from pyc3l.wallet import Wallet

    password = None
    if password_file:
        password = file_get_contents(password_file)
        password = re.sub(r"\r?\n?$", "", password)  ## remove ending newline if any

    wallet = Wallet(file_get_contents(keyfile), endpoint=ctx._endpoint)

    ctx.verbose(
        "Opened wallet %s on currency %s"
        % (
            click.style(f"0x{wallet.data['address']}", fg="cyan"),
            click.style(wallet.data["server"]["name"], fg="magenta", bold=True),
        )
    )

    while True:
        if not password:
            password = getpass.getpass("  password: ")

        try:
            wallet.unlock(password)
        except ValueError:
            ctx.err("invalid password...")
            if password_file:
                exit(1)
            password = None
            continue
        break

    ctx.verbose(
        "  Unlocked %s." % (click.style("successfully", fg="green", bold=True),)
    )

    print("yay")

    pyc3l = Pyc3l(ctx._currency, endpoint=ctx._endpoint)
    exit(0)


# run()
# exit(0)

# # Load the API
# print('INFO: Load the API.')
# api_handling = ApiHandling()

# account_opener = LocalAccountOpener()
# server, sender_account = account_opener.openAccountInteractively('Select Admin Wallet',account_file=account_file, password=password)

# #load the high level functions
# print('INFO: load the high level functions.')
# api_com = ApiCommunication(api_handling, server)


# print('INFO: Check the provided account to have admin role.')
# api_com.checkAdmin(sender_account.address)
# Sender_status = api_com.getAccountIsActive(sender_account.address)

# if not Sender_status:
#     print("Error: The Admin Wallet is locked!")
#     sys.exit()
