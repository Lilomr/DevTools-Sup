import dns.name
import dns.resolver
from flask import Flask, render_template, request, send_file
import socket
import dns

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

@app.route("/porta", methods=["GET"])
def portaConstructor():
    ctx = {}
    ctx["meuIp"] = cs.getInicialPage()
    ctx["ip"] = cs.getInicialPage()
    ctx["porta"] = '80'
    return render_template("portapage.html", **ctx)
    
@app.route("/porta", methods=["POST"])
def receberPorta():
    ctx = {}
    try:
        #SET DADOS FORMULARIO
        ctx["meuIp"] = cs.getInicialPage()
        #RECEBE DADOS DO FORMULARIO
        ip = request.form.get("ip")
        portas = request.form.get("porta")
        #CONSULTA PORTA (UMA OU MAIS PORTAS)
        result = []
        result = cs.consultaPortas(ip, portas)
        portaP = result[0]
        statusP = result[1]
        colorP = result[2]
        #PREENCHE CONTEXTO PARA RETORNAR A PAGINA
        ctx["porta"] = portaP[0]
        ctx["status"] = statusP[0]
        ctx["color"] = colorP[0]
        ctx["ip"] = ip
        ctx["ip2"] = cs.socket.gethostbyname(ip)

    except socket.gaierror:
        ctx["status"] = f"Servidor {ip} Inválido"
    #except TypeError as e:
    #    ctx["status"] = f"Porta {porta} Inválida"
    #except OverflowError:
    #    ctx["status"] = f"Porta {porta} Inválida"

    return render_template("portapage.html", **ctx)


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
        statusRota = []
        statusRota = cs.consultaRotaDns(ip)
        ctx["status"] = statusRota
    except dns.resolver.NoAnswer:
        ctx["status"] = "Sem resposta"
    except dns.resolver.NXDOMAIN:
        ctx["status"] = "DNS Inválido"
    except dns.name.EmptyLabel:
        ctx["status"] = "DNS Inválido"

    return render_template("dnspage.html", **ctx)

##################################################################################################

@app.route("/combo", methods=["GET"])
def comboConstructor():
    ctx = {}
    ctx["meuIp"] = cs.getInicialPage()
    ctx["ip"] = cs.getInicialPage()
    ctx["portas"] = '8181,5432'
    return render_template("combopage.html", **ctx)

@app.route("/combo", methods=["POST"])
def receberCombo():
    ctx = {}
    try:
        #SET DADOS FORMULARIO
        ctx["meuIp"] = cs.getInicialPage()
        #RECEBE DADOS DO FORMULARIO
        ip = request.form.get("ip")
        portas = request.form.get("portas")
        #CONSULTA PORTA (UMA OU MAIS PORTAS)
        result = []
        result = cs.consultaPortas(ip, portas)
        portaP = result[0]
        statusP = result[1]
        colorP = result[2]
        #PREENCHE CONTEXTO PARA RETORNAR A PAGINA
        ctx["portaP"] = portaP
        ctx["statusP"] = statusP
        ctx["colorP"] = colorP
        ctx["ip"] = ip
        ctx["ip2"] = cs.socket.gethostbyname(ip)
        ctx["portas"] = portas
        #VERIFICA ROTA DNS
        statusRota = []
        statusRota = cs.consultaRotaDns(ip)
        ctx["statusRota"] = statusRota

    except socket.gaierror:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    except UnicodeError:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    #except TypeError as e:
    #    ctx[f"statusP"] = f"Porta {porta} Inválida"
    #except OverflowError:
    #    ctx[f"statusP"] = f"Porta {porta} Inválida"
    except dns.resolver.NoAnswer:
        ctx["statusRota"] = "Sem resposta"
    except dns.resolver.NXDOMAIN:
        ctx["statusRota"] = "DNS Inválido"
    except dns.name.EmptyLabel:
        ctx["statusRota"] = "DNS Inválido"

    return render_template("combopage.html", **ctx)

##################################################################################################

@app.route("/teste", methods=["GET"])
def testeConstructor():
    ctx = {}
    ctx["meuIp"] = cs.getInicialPage()
    ctx["ip"] = cs.getInicialPage()
    ctx["portas"] = '8181,5432'
    return render_template("testepage.html", **ctx)

@app.route("/teste", methods=["POST"])
def receberTeste():
    ctx = {}
    try:
        #SET DADOS FORMULARIO
        ctx["meuIp"] = cs.getInicialPage()
        #RECEBE DADOS DO FORMULARIO
        ip = request.form.get("ip")
        portas = request.form.get("portas")
        #CONSULTA PORTA (UMA OU MAIS PORTAS)
        result = []
        result = cs.consultaPortas(ip, portas)
        portaP = result[0]
        statusP = result[1]
        colorP = result[2]
        #PREENCHE CONTEXTO PARA RETORNAR A PAGINA
        ctx["portaP"] = portaP
        ctx["statusP"] = statusP
        ctx["colorP"] = colorP
        ctx["ip"] = ip
        ctx["ip2"] = cs.socket.gethostbyname(ip)
        ctx["portas"] = portas
        #VERIFICA ROTA DNS
        statusRota = []
        statusRota = cs.consultaRotaDns(ip)
        ctx["statusRota"] = statusRota

    except socket.gaierror:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    except UnicodeError:
        ctx["statusIp"] = f"Servidor {ip} Inválido"
    #except TypeError as e:
    #    ctx[f"statusP"] = f"Porta {porta} Inválida"
    #except OverflowError:
    #    ctx[f"statusP"] = f"Porta {porta} Inválida"
    except dns.resolver.NoAnswer:
        ctx["statusRota"] = "Sem resposta"
    except dns.resolver.NXDOMAIN:
        ctx["statusRota"] = "DNS Inválido"
    except dns.name.EmptyLabel:
        ctx["statusRota"] = "DNS Inválido"

    return render_template("testepage.html", **ctx)

if __name__ == "__main__":
    app.run(debug=True)
