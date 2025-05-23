import socket
import dns
import dns.name
import dns.resolver

def consultaPortas(ip, portas):
        result = []
        portaP = []
        statusP = []
        colorP = []
        for porta in portas.split(','):
            if int(porta) <= 65535 and port(ip, int(porta)) == True:
                portaP.append(f"{porta}")
                statusP.append(f"Aberta")
                colorP.append(f"green")
            else :
                portaP.append(f"{porta}")
                statusP.append(f"Fechada")
                colorP.append(f"red")
        result.append(portaP)
        result.append(statusP)
        result.append(colorP)
        return result


def port(endereco, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((endereco, porta))
    sock.close()
    return result == 0

def consultaRotaDns(ip):
    name = dns.name.from_text(ip)
    resposta = dns.resolver.resolve(name)
    
    #CRIA LISTA DE ROTAS
    if resposta:
        statusRota = []

        for answer in resposta.response.answer:
            for item in answer.items:
                if item.rdtype == dns.rdatatype.A:
                    statusRota.append(item.address)
                elif item.rdtype == dns.rdatatype.CNAME:
                    statusRota.append(str(answer.name).strip('.'))
                    statusRota.append(str(item.target).strip('.'))
                else:
                    statusRota.append(item.to_text())
    return statusRota