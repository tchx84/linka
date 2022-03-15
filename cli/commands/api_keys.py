import click

from typing import Optional
from tabulate import tabulate

from app import models
from app.db import db
from cli.decorators import coro


@click.group()
def api_keys() -> None:
    """API Keys management"""
    pass


@api_keys.command(name="list")
@coro
async def list_() -> None:
    """List current origins registered with an API Key"""
    origins = await models.APIKey.get_origins(db)
    click.echo(
        tabulate(
            origins,
            headers=["Origin", "Number of registered API Keys"],
        )
    )


@api_keys.command()
@click.argument("origin")
@coro
async def create(origin: str) -> None:
    """Create a new API Key"""
    api_key = await models.APIKey.create_new_key(db, origin)
    click.echo(f"Your new API key is: {api_key}")


@api_keys.command()
@click.argument("origin")
@click.option("--key", help="API Key to be removed")
@click.option(
    "--all",
    "all_",
    is_flag=True,
    default=False,
    help="Remove all keys for the provided origin",
)
@coro
async def revoke(origin: str, key: Optional[str], all_: Optional[bool]) -> None:
    """Revoke one or all API Key(s) for a specific origin"""
    if not any([key, all_]):
        raise click.UsageError("--key or --all must be provided")
    if all([key, all_]):
        raise click.UsageError("Provide either --key or --all but not both.")

    if key:
        if await models.APIKey.revoke_key(db, origin, key):
            click.echo("API Key revoked.")
        else:
            click.echo("Couldn't remove the provide API Key.")
    if all_:
        if await models.APIKey.revoke_all_keys(db, origin):
            click.echo(f"All API keys for '{origin}'' have been revoked.")
        else:
            click.echo(f"Couldn't remove the API keys for {origin}.")
