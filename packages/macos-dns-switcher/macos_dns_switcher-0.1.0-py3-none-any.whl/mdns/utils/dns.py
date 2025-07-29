# DNS Options
import subprocess

DNS_CHOICES = {
    "default": {
        "v4": [],
        "v6": [],
    },
    "OpenDNS": {
        "v4": ["208.67.222.222", "208.67.220.220"],
        "v6": ["2620:119:35::35", "2620:119:53::53"],
    },
    "CloudFlare": {
        "v4": ["1.1.1.1", "1.0.0.1"],
        "v6": ["2606:4700:4700::1111", "2606:4700:4700::1001"],
    },
    "Quad9": {"v4": ["9.9.9.9", "9.9.9.10"], "v6": ["2620:fe::9", "2620:fe::10"]},
}


def set_dns(service, dns_v4, dns_v6):
    if not dns_v4 and not dns_v6:
        subprocess.run(["networksetup", "-setdnsservers", service, "Empty"])
        print(f"✅ Reset DNS to default for {service}")
    else:
        combined_dns = dns_v4 + dns_v6
        subprocess.run(["networksetup", "-setdnsservers", service] + combined_dns)
        print(f"✅ Set DNS to {', '.join(combined_dns)} for {service}")
