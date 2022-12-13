import click

from pydolphinscheduler import configuration
from pydolphinscheduler.models.tenant import Tenant


@click.help_option()
def tenants() -> click.group:
    """Users subcommand group."""


@click.group()
def tenants() -> click.group:
    """Users subcommand group."""


@tenants.command()
@click.option(
    "-n", "--name", "name",
    required=True,
    type=str,
)
@click.option(
    "-q", "--queue-name", "queue_name",
    required=True,
    type=str,
)
@click.option(
    "-d", "--description", "description",
    required=True,
    type=str,
)
def create(name, queue_name, description):
    tenant = Tenant.get(name)
    if tenant:
        click.echo(f"Tenant with name {name} already exists.", err=True)
    new_tenant = Tenant.create(name, queue_name, description)
    click.echo(f"Tenant {new_tenant.name} had been created.")


@tenants.command()
@click.option(
    "-n", "--name", "name",
    required=True,
    type=str,
)
def delete(name):
    tenant = Tenant.delete(name)
    if not tenant:
        click.echo(f"Tenant with name {name} not exists.", err=True)
    click.echo(f"Tenant: {tenant}.")


@tenants.command()
@click.option(
    "-n", "--name", "name",
    required=True,
    type=str,
)
def get(name):
    tenant = Tenant.get(name)
    if not tenant:
        click.echo(f"Tenant with name {name} not exists.", err=True)
    click.echo(f"Tenant: {tenant}.")
