import click
import uuid
import hashlib

from app.db import db
from app.schemas import APIKey
from app import models

from cli.decorators import coro
from tabulate import tabulate


@click.group()
def api_keys() -> None:
    """API Keys management"""
    pass


@api_keys.command(name="list")
@coro
async def list_() -> None:
    """ List current applications registered with an API Key """
    apps = await models.APIKey.get_apps(db)
    click.echo(
            tabulate(
                apps,
                headers=["Application", "Prefix"],
                tablefmt="grid",
            )
        )


@api_keys.command()
@click.argument('application')
@coro
async def create(application: str) -> None:
    """Create a new API Key"""
    prefix = uuid.uuid4().hex[:7]
    raw_api_key = uuid.uuid4().hex
    api_key_hash = hashlib.sha256(raw_api_key.encode('utf-8')).hexdigest()

    api_key = APIKey(application=application, prefix=prefix, api_key_hash=api_key_hash)
    await models.APIKey.store(db, api_key.dict())
    click.echo(f"Your new API key is: {prefix}.{raw_api_key}")


@api_keys.command()
@click.argument('application')
@click.argument('prefix')
@coro
async def revoke(application: str, prefix: str) -> None:
    """Revoke an API Key for a specific prefix/application"""
    api_key = APIKey(application=application, prefix=prefix)
    await models.APIKey.delete(db, api_key.dict())
    click.echo("Done. API Key revoked.")
