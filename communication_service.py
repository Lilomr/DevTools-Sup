import socket

import dns.name
import dns.rdatatype
import dns.resolver


def get_client_ip(request) -> str | None:
    return (
        request.headers.get("X-Forwarded-For")
        or request.headers.get("X-Real-IP")
        or request.headers.get("Remote-Addr")
    )


def check_port(address: str, port: int, timeout: float = 3.0) -> bool:
    """Testa uma porta TCP. Suporta IPv4, IPv6 e hostnames."""
    try:
        with socket.create_connection((address, port), timeout=timeout):
            return True
    except OSError:
        return False


def check_ports(ip: str, ports_str: str) -> tuple[list, list, list]:
    port_list, status_list, color_list = [], [], []

    for raw in ports_str.split(","):
        porta = raw.strip()
        if not porta:
            continue
        if not porta.isdigit() or not (1 <= int(porta) <= 65535):
            port_list.append(porta)
            status_list.append("Inválida")
            color_list.append("resultColorInvalid")
        elif check_port(ip, int(porta)):
            port_list.append(porta)
            status_list.append("Aberta")
            color_list.append("resultColorOpen")
        else:
            port_list.append(porta)
            status_list.append("Fechada")
            color_list.append("resultColorClose")

    return port_list, status_list, color_list


def resolve_dns(hostname: str) -> list[str]:
    name = dns.name.from_text(hostname)
    response = dns.resolver.resolve(name)
    records: list[str] = []

    for answer in response.response.answer:
        for item in answer.items:
            if item.rdtype == dns.rdatatype.A:
                records.append(item.address)
            elif item.rdtype == dns.rdatatype.CNAME:
                records.append(str(answer.name).strip("."))
                records.append(str(item.target).strip("."))
            else:
                records.append(item.to_text())

    return records
