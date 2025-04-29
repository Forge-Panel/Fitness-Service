#!./venv/bin/python

import click
import os
import sys

file_dir = os.path.dirname('models')
sys.path.append(file_dir)

from add import add
from seed import seed

print(r"""
 ______ ____  _____   _____ ______ 
|  ____/ __ \|  __ \ / ____|  ____|
| |__ | |  | | |__) | |  __| |__   
|  __|| |  | |  _  /| | |_ |  __|  
| |   | |__| | | \ \| |__| | |____ 
|_|    \____/|_|  \_\\_____|______| CLI
""")


@click.group()
def cli():
    pass


cli.add_command(add)
cli.add_command(seed)


if __name__ == '__main__':
    cli()
    print()
