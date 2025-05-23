import dns.name
import dns.resolver
from flask import Flask, render_template, request, send_file
import socket
import dns

app = Flask(__name__, template_folder="Templates")


@app.route("/")
def index():
    print(request.headers)
    return render_template("homepage.html")


@app.route("/Estilizacao/<path:path>")
def send_js(path):
    return send_file("Estilizacao/" + path)


@app.route("/porta", methods=["GET"])
def portaConstructor():
    meuIp = (
        request.headers.get("X-Forwarded-For")
        or request.headers.get("X-Real-IP")
        or request.headers.get("Remote-Addr")
    )
    return render_template("portapage.html", meuIp=meuIp, ip=meuIp, porta=80)


def port(endereco, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    result = sock.connect_ex((endereco, porta))
    sock.close()
    return result == 0


@app.route("/porta", methods=["POST"])
def receberPorta():
    ctx = {}
    try:
        statusPorta = None
        ctx["meuIp"] = (
            request.headers.get("X-Forwarded-For")
            or request.headers.get("X-Real-IP")
            or request.headers.get("Remote-Addr")
        )
        ip = request.form.get("ip")
        ctx["ip"] = ip
        porta = request.form.get("porta", type=int)
        ctx["porta"] = porta
        statusPorta = port(ip, porta)
        ctx["ip"] = socket.gethostbyname(ip)
        ctx["ip2"] = ip

    except socket.gaierror:
        ctx["status"] = f"Servidor {ip} Inválido"
    except TypeError as e:
        ctx["status"] = f"Porta {porta} Inválida"
    except OverflowError:
        ctx["status"] = f"Porta {porta} Inválida"

    if statusPorta == True:
        ctx["status"] = "Aberta"
        ctx["color"] = "green"

    elif statusPorta == False:
        ctx["status"] = "Fechada"
        ctx["color"] = "red"

    return render_template("portapage.html", **ctx)


##################################################################################################


@app.route("/dns", methods=["POST"])
def receberDns():
    ctx = {}
    endereço = request.form.get("dns")
    ctx["dns"] = endereço
    resposta = None

    try:
        name = dns.name.from_text(endereço)
        resposta = dns.resolver.resolve(name)
    except dns.resolver.NoAnswer:
        ctx["status"] = "Sem resposta"
    except dns.resolver.NXDOMAIN:
        ctx["status"] = "DNS Inválido"
    except dns.name.EmptyLabel:
        ctx["status"] = "DNS Inválido"
    if resposta:
        ctx["status"] = "\n".join([a.to_text() for a in resposta.response.answer])
    return render_template("dnspage.html", **ctx)


@app.route("/dns", methods=["GET"])
def dnsConstructor():
    return render_template("dnspage.html")

##################################################################################################

@app.route("/combo", methods=["GET"])
def comboConstructor():
    meuIp = (
        request.headers.get("X-Forwarded-For")
        or request.headers.get("X-Real-IP")
        or request.headers.get("Remote-Addr")
    )
    portas = '8181,5432'
    return render_template("combopage.html", meuIp=meuIp, ip=meuIp, portas=portas)

@app.route("/combo", methods=["POST"])
def receberCombo():
    ctx = {}
    try:
        #SET DADOS FORMULARIO
        ctx["meuIp"] = (
            request.headers.get("X-Forwarded-For")
            or request.headers.get("X-Real-IP")
            or request.headers.get("Remote-Addr")
        )
        ip = request.form.get("ip")
        portas = request.form.get("portas")

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

        ctx["portaP"] = portaP
        ctx["statusP"] = statusP
        ctx["colorP"] = colorP

        ctx["ip"] = ip
        ctx["ip2"] = socket.gethostbyname(ip)
        ctx["portas"] = portas
        
        #VERIFICA DNS
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
            ctx["statusRota"] = statusRota

    except socket.gaierror:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    except UnicodeError:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    except TypeError as e:
        ctx[f"statusP"] = f"Porta {porta} Inválida"
    except OverflowError:
        ctx[f"statusP"] = f"Porta {porta} Inválida"
    except dns.resolver.NoAnswer:
        ctx["statusRota"] = "Sem resposta"
    except dns.resolver.NXDOMAIN:
        ctx["statusRota"] = "DNS Inválido"
    except dns.name.EmptyLabel:
        ctx["statusRota"] = "DNS Inválido"

    return render_template("combopage.html", **ctx)

if __name__ == "__main__":
    app.run(debug=True)
