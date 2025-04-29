import click
from .user import user


@click.group()
def add():
    pass


add.add_command(user)
