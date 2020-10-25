import click

from .commands.api_keys import api_keys


@click.group()
def main() -> None:
    """Main CLI for linka server side operations"""


main.add_command(api_keys)
