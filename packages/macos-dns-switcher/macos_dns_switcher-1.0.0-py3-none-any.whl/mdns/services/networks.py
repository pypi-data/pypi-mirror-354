import subprocess


def list_network_services():
    result = subprocess.run(
        ["networksetup", "-listallnetworkservices"], capture_output=True, text=True
    )
    lines = result.stdout.strip().split("\n")

    # Filter out header and disabled services
    services = [
        line.strip()
        for line in lines
        if line and not line.startswith("*") and "denotes" not in line
    ]
    return services
