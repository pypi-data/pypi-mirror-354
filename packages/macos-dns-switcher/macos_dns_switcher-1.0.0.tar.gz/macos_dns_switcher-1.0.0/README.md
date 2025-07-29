# 🛜🍎 macOS DNS Switcher (Python)

A command-line utility to programmatically change the DNS settings of your macOS network services using Python and
`networksetup`. It is based on [Yggland datas](https://yggland.fr/FAQ-Tutos/).

---

## ✨ Features

- Choose from pre-configured public DNS providers:
    - **OpenDNS**
    - **Cloudflare**
    - **Quad9**
    - Or reset to **default**
- Supports both **IPv4** and **IPv6** addresses
- Configure one or multiple **network services** (e.g., `Wi-Fi`, `Ethernet`, `iPhone USB`)
- Easily reset DNS to DHCP-provided values

---

## 🛠 Requirements

- macOS
- Python 3.7+
- Admin privileges (`sudo` required to change network settings)

---

## 🚀 Installation

You can install via `pip` (if published on PyPI):

```bash
pip install macos-dns-switcher
```

Or install from source:

```bash
git clone https://github.com/JimmyMtl/macos-dns-switcher.git
cd macos-dns-switcher
pip install .
```

---

## ▶️ Usage

Run the CLI tool with:

```bash
sudo mdns
```

### 🧭 Interactive Flow

1. Select one or more network services (e.g., Wi-Fi, Ethernet)
2. Choose a DNS provider:
    - `0` – Default (reset to DHCP)
    - `1` – OpenDNS
    - `2` – Cloudflare
    - `3` – Quad9
3. The tool applies the selected DNS settings to all selected services

---

## 🔍 Verifying DNS Settings

To confirm the DNS settings applied to a service:

```bash
networksetup -getdnsservers "Wi-Fi"
```

Replace `"Wi-Fi"` with your actual service name if different.

---

## 🧼 Reset DNS to Default

To remove custom DNS settings and restore DHCP:

```bash
sudo mdns
```

Then:
- Select the target service(s)
- Choose option `0` to reset

---

## 🛡️ Notes & Warnings

- Only works on **macOS** via `networksetup`
- DNS settings apply system-wide and may not persist if overwritten by VPNs or profiles

---

## 📄 License

MIT License

---

## 🙋 Support

Feel free to open an issue or submit a pull request if you’d like to contribute or request a feature!
