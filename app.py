from flask import Flask,render_template,request,send_file
import socket

app = Flask(__name__, template_folder='Templates')

@app.route('/')
def index():
    print(request.headers)
    return render_template('Entrada.html')

@app.route('/Estilizacao/<path:path>')
def send_js(path):
    return send_file('Estilizacao/' + path)

@app.route('/porta', methods=['GET'])
def TestePorta():
    meuIp = (request.headers.get('X-Forwarded-For') or  
    request.headers.get('X-Real-IP') or 
    request.headers.get('Remote-Addr'))
    return render_template('TestePorta.html',meuIp = meuIp, ip = meuIp, porta = 80) 

def port(endereco,porta):    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3)
    result = sock.connect_ex((endereco, porta))
    sock.close()
    return result == 0

@app.route('/porta', methods=['POST'])
def receberPorta():
    try:
        meuIp = (request.headers.get('X-Forwarded-For') or  
            request.headers.get('X-Real-IP') or 
            request.headers.get('Remote-Addr'))
        porta = request.form.get('porta',type=int)
        ip = request.form.get('ip')
        status = port(ip,porta)
        ip = socket.gethostbyname(ip) 

    except socket.gaierror:
        return render_template('TestePorta.html',
                                ip = ip,
                                porta = porta,
                                meuIp = meuIp,
                                status = f'Servidor {ip} Inválido',)
    except TypeError as e:
        return render_template('TestePorta.html', ip = ip,
                                porta = porta,
                                meuIp = meuIp,
                                status = f'Porta {porta} Inválida')
    except OverflowError:
        return render_template('TestePorta.html',ip = ip,
                                porta = porta,
                                meuIp = meuIp,
                                status = f'Porta {porta} Inválida')
        
        
    if status == True:        
        return render_template('TestePorta.html',ip = ip,
            porta = porta,
            status = 'Aberta',
            meuIp = meuIp,
            color = 'green')
        
    else:
        return render_template('TestePorta.html', ip = ip,
            porta = porta,
            status = 'Fechada',
            meuIp = meuIp,
            color = 'red')
    
if __name__ == '__main__':
    app.run(debug=True)

    