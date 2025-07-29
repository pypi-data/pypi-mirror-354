#!/usr/bin/env python


import click

from pyc3l import Pyc3l


@click.command()
@click.option("-e", "--endpoint", help="Force com-chain endpoint.")
def run(endpoint):
    pyc3l = Pyc3l(endpoint)
    current_block = pyc3l.endpoint.api.post()
    print(f"Current block: {current_block}")
