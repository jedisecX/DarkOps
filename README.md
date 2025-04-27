
# DarkOps Stress Suite

> Multi-Protocol Network Stress Tester for authorized testing and research purposes only.

---
## Features

- **UDP Flood** – Raw datagram packet overload
- **TCP SYN Flood** – Connection half-open exhaustion
- **HTTP Flood** – Layer 7 web server saturation
- **SSL Renegotiation Attack** – TLS handshake CPU exhaustion
- **Slowloris Attack** – Socket drip starvation
- **ICMP Flood** – Raw ping flood
- **DNS Amplification** – Reflection attack leveraging DNS servers
- **Dynamic Attack Rotation** – Attacks randomly rotate during operation
- **Proxy Support** – SOCKS4, SOCKS5, HTTP proxies
- **SSL/TLS Support** – Full HTTPS flood capabilities
- **Custom Payloads** – Randomly updating payloads per request
- **Multi-threaded** – Scale attacks with adjustable thread counts

---
## Installation

```bash
pip install -r requirements.txt
```

Requirements:
- Python 3.8+
- Modules: socks, requests, dnspython, scapy

---
## Usage

```bash
python3 DarkOpsStressSuite.py
```

You will be prompted for:
- Target IP/Hostname
- Port
- Duration
- Number of Threads
- Use SSL/TLS? (y/n)
- Use Proxy List? (y/n)

**Proxy List Format:**
```
IP:PORT
IP:PORT
```

Example: proxies.txt

---
## Legal Disclaimer

This tool is designed for authorized stress testing and educational research only.
Unauthorized use against systems you do not own is illegal and punishable by law.

By using this tool, you agree to use it responsibly.

---
## Author
**Jedi Security | DarkOps Team**
Website: [https://jedi-sec.com](https://jedi-sec.com)
