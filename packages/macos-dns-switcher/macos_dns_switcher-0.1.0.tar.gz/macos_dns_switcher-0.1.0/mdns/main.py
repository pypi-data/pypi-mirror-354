from services.networks import list_network_services
from utils.dns import DNS_CHOICES, set_dns


def choose_services(services):
    print("\nAvailable network services:")
    for idx, service in enumerate(services):
        print(f"{idx}. {service}")

    choices = input(
        "Enter the numbers of the services you want to configure (comma-separated): "
    )
    selected = []
    for choice in choices.split(","):
        try:
            idx = int(choice.strip())
            if 0 <= idx < len(services):
                selected.append(services[idx])
        except ValueError:
            pass

    return selected


def choose_dns_provider():
    print("\nChoose DNS provider:")
    for idx, provider in enumerate(DNS_CHOICES):
        print(f"{idx}. {provider}")
    choice = int(input("Enter your choice: "))
    return list(DNS_CHOICES.keys())[choice]


def main():
    services = list_network_services()
    if not services:
        print("No available network services found.")
        return

    selected_services = choose_services(services)
    if not selected_services:
        print("No services selected.")
        return

    provider = choose_dns_provider()
    dns_v4 = DNS_CHOICES[provider]["v4"]
    dns_v6 = DNS_CHOICES[provider]["v6"]

    for service in selected_services:
        set_dns(service, dns_v4, dns_v6)


if __name__ == "__main__":
    main()
