import dns.name
import dns.resolver
from flask import Flask, render_template, request, send_file
import socket
import dns
import difflib

import communication_service as cs

app = Flask(__name__, template_folder="Templates")


@app.route("/")
def index():
    print(request.headers)
    return render_template("homepage.html")


@app.route("/Estilizacao/<path:path>")
def send_js(path):
    return send_file("Estilizacao/" + path)


##################################################################################################


@app.route("/dns", methods=["GET"])
def dnsConstructor():
    return render_template("dnspage.html")


@app.route("/dns", methods=["POST"])
def receberDns():
    ctx = {}
    try:
        ip = request.form.get("dns")
        ctx["dns"] = ip
        statusRota = cs.consultaRotaDns(ip)
        ctx["status"] = statusRota
    except dns.resolver.NoAnswer:
        ctx["status"] = ["Sem resposta"]
    except dns.resolver.NXDOMAIN:
        ctx["status"] = ["DNS Inválido"]
    except dns.name.EmptyLabel:
        ctx["status"] = ["DNS Inválido"]
    except Exception as e:
        ctx["status"] = [f"Erro: {str(e)}"]
    return render_template("dnspage.html", **ctx)


##################################################################################################


@app.route("/combo", methods=["GET"])
def comboConstructor():
    ctx = {}
    ctx["meuIp"] = cs.getInicialPage()
    ctx["ip"] = cs.getInicialPage()
    ctx["portas"] = "8181,5432"
    return render_template("combopage.html", **ctx)


@app.route("/combo", methods=["POST"])
def receberCombo():
    ctx = {}
    try:
        # SET DADOS FORMULARIO
        ctx["meuIp"] = cs.getInicialPage()
        # RECEBE DADOS DO FORMULARIO
        ip = request.form.get("ip")
        portas = request.form.get("portas")
        # CONSULTA PORTA (UMA OU MAIS PORTAS)
        result = []
        result = cs.consultaPortas(ip, portas)
        portaP = result[0]
        statusP = result[1]
        colorP = result[2]
        # PREENCHE CONTEXTO PARA RETORNAR A PAGINA
        ctx["portaP"] = portaP
        ctx["statusP"] = statusP
        ctx["colorP"] = colorP
        ctx["ip"] = ip
        ctx["ip2"] = cs.socket.gethostbyname(ip)
        ctx["portas"] = portas
        # VERIFICA ROTA DNS
        statusRota = []
        statusRota = cs.consultaRotaDns(ip)
        ctx["statusRota"] = statusRota

    except socket.gaierror:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    except UnicodeError:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    # except TypeError as e:
    #    ctx[f"statusP"] = f"Porta {porta} Inválida"
    # except OverflowError:
    #    ctx[f"statusP"] = f"Porta {porta} Inválida"
    except dns.resolver.NoAnswer:
        ctx["statusRota"] = "Sem resposta"
    except dns.resolver.NXDOMAIN:
        ctx["statusRota"] = "DNS Inválido"
    except dns.name.EmptyLabel:
        ctx["statusRota"] = "DNS Inválido"

    ctx["css"] = "boxResult"

    return render_template("combopage.html", **ctx)


##################################################################################################


@app.route("/teste", methods=["POST"])
def receberTeste():
    ctx = {}
    try:
        # SET DADOS FORMULARIO
        ctx["meuIp"] = cs.getInicialPage()
        # RECEBE DADOS DO FORMULARIO
        ip = request.form.get("ip")
        portas = request.form.get("portas")
        # CONSULTA PORTA (UMA OU MAIS PORTAS)
        result = []
        result = cs.consultaPortas(ip, portas)
        portaP = result[0]
        statusP = result[1]
        colorP = result[2]
        # PREENCHE CONTEXTO PARA RETORNAR A PAGINA
        ctx["portaP"] = portaP
        ctx["statusP"] = statusP
        ctx["colorP"] = colorP
        ctx["ip"] = ip
        ctx["ip2"] = cs.socket.gethostbyname(ip)
        ctx["portas"] = portas
        # VERIFICA ROTA DNS
        statusRota = []
        statusRota = cs.consultaRotaDns(ip)
        ctx["statusRota"] = statusRota

    except socket.gaierror:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    except UnicodeError:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    # except TypeError as e:
    #    ctx[f"statusP"] = f"Porta {porta} Inválida"
    # except OverflowError:
    #    ctx[f"statusP"] = f"Porta {porta} Inválida"
    except dns.resolver.NoAnswer:
        ctx["statusRota"] = "Sem resposta"
    except dns.resolver.NXDOMAIN:
        ctx["statusRota"] = "DNS Inválido"
    except dns.name.EmptyLabel:
        ctx["statusRota"] = "DNS Inválido"

    ctx["css"] = """.boxResult {
    display: block;
    }"""

    return render_template("testepage.html", **ctx)


##################################################################################################


@app.route("/diff", methods=["GET", "POST"])
def diff_get():
    if request.method == "GET":
        return render_template("diffpage.html")
    ctx = {}
    input1 = request.form.get("input1", "")
    input2 = request.form.get("input2", "")
    diffs = list(difflib.ndiff(input1.splitlines(), input2.splitlines()))
    resultado1 = []
    resultado2 = []
    for line in diffs:
        if line.startswith("- "):
            resultado1.append((line, "red"))
            resultado2.append(("", ""))
        elif line.startswith("+ "):
            resultado1.append(("", ""))
            resultado2.append((line, "green"))
        elif line.startswith("? "):
            continue
        else:
            resultado1.append((line, "black"))
            resultado2.append((line, "black"))
    ctx["resultado1"] = enumerate(resultado1, 1)
    ctx["resultado2"] = enumerate(resultado2, 1)
    ctx["input1"] = input1
    ctx["input2"] = input2
    return render_template("diffpage.html", **ctx)


if __name__ == "__main__":
    app.run(debug=True)
