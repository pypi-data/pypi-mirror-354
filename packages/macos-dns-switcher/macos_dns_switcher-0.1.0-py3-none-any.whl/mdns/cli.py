# mycli/cli.py

# from mdns.services.networks import list_network_services
from mdns.utils.dns import DNS_CHOICES, set_dns
import click

from mdns.services.networks import list_network_services


@click.command()
def main():
    services = list_network_services()
    if not services:
        click.echo("No available network services found.")
        return

    click.echo("\nAvailable network services:")
    for idx, service in enumerate(services):
        click.echo(f"{idx}. {service}")

    choices = click.prompt(
        "Enter the numbers of the services you want to configure (comma-separated)",
        type=str
    )
    selected = []
    for choice in choices.split(","):
        try:
            idx = int(choice.strip())
            if 0 <= idx < len(services):
                selected.append(services[idx])
        except ValueError:
            pass

    if not selected:
        click.echo("No services selected.")
        return

    click.echo("\nChoose DNS provider:")
    for idx, provider in enumerate(DNS_CHOICES):
        click.echo(f"{idx}. {provider}")
    provider_index = click.prompt("Enter your choice", type=int)
    provider = list(DNS_CHOICES.keys())[provider_index]

    dns_v4 = DNS_CHOICES[provider]["v4"]
    dns_v6 = DNS_CHOICES[provider]["v6"]

    for service in selected:
        set_dns(service, dns_v4, dns_v6)
        click.echo(f"DNS updated for {service}")


if __name__ == "__main__":
    main()
