import dns.name
import dns.resolver
from flask import Flask, render_template, request, send_file
import socket
import dns

app = Flask(__name__, template_folder="Templates")


@app.route("/")
def index():
    print(request.headers)
    return render_template("Entrada.html")


@app.route("/Estilizacao/<path:path>")
def send_js(path):
    return send_file("Estilizacao/" + path)


@app.route("/porta", methods=["GET"])
def TestePorta():
    meuIp = (
        request.headers.get("X-Forwarded-For")
        or request.headers.get("X-Real-IP")
        or request.headers.get("Remote-Addr")
    )
    return render_template("TestePorta.html", meuIp=meuIp, ip=meuIp, porta=80)


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

    return render_template("TestePorta.html", **ctx)


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
    return render_template("TesteDns.html", **ctx)


@app.route("/dns", methods=["GET"])
def TesteDns():
    return render_template("TesteDns.html")

##################################################################################################

@app.route("/combo", methods=["GET"])
def TesteCombo():
    meuIp = (
        request.headers.get("X-Forwarded-For")
        or request.headers.get("X-Real-IP")
        or request.headers.get("Remote-Addr")
    )
    return render_template("TesteCombo.html", meuIp=meuIp, ip=meuIp, porta1=8181, porta2=5432)

@app.route("/combo", methods=["POST"])
def receberCombo():
    ctx = {}
    try:
        #SET STATUS BLOQUEADO
        ctx["statusP1"] = "Fechada"
        ctx["colorP1"] = "red"
        ctx["statusP2"] = "Fechada"
        ctx["colorP2"] = "red"

        #SET DADOS FORMULARIO
        ctx["meuIp"] = (
            request.headers.get("X-Forwarded-For")
            or request.headers.get("X-Real-IP")
            or request.headers.get("Remote-Addr")
        )
        ip = request.form.get("ip")
        porta1 = request.form.get("porta1", type=int)
        porta2 = request.form.get("porta2", type=int)
        ctx["ip"] = ip
        ctx["porta1"] = porta1
        ctx["porta2"] = porta2
        ctx["ip2"] = socket.gethostbyname(ip)
        

        #VERIFICA PORTAS
        if port(ip, porta1) == True:
            ctx["statusP1"] = "Aberta"
            ctx["colorP1"] = "green"

        if port(ip, porta2) == True:
            ctx["statusP2"] = "Aberta"
            ctx["colorP2"] = "green"

        #VERIFICA DNS
        name = dns.name.from_text(ip)
        resposta = dns.resolver.resolve(name)
        
        #CRIA LISTA DE ROTAS
        if resposta:
            rota = [a.to_text() for a in resposta.response.answer]
            statusRota = []
            for i in range(len(rota)):
                statusRota.append(rota[i].split('. ')[0])
            statusRota.append(rota[i].split('A ')[1])
            ctx["statusRota"] = statusRota

    except socket.gaierror:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    except TypeError as e:
        ctx["statusP1"] = f"Porta {porta1} Inválida"
    except OverflowError:
        ctx["statusP1"] = f"Porta {porta1} Inválida"
    except TypeError as e:
        ctx["statusP2"] = f"Porta {porta2} Inválida"
    except OverflowError:
        ctx["statusP2"] = f"Porta {porta2} Inválida"
    except dns.resolver.NoAnswer:
        ctx["statusRota"] = "Sem resposta"
    except dns.resolver.NXDOMAIN:
        ctx["statusRota"] = "DNS Inválido"
    except dns.name.EmptyLabel:
        ctx["statusRota"] = "DNS Inválido"

    return render_template("TesteCombo.html", **ctx)

if __name__ == "__main__":
    app.run(debug=True)
