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


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
