from flask import Flask,render_template,request
import socket

app = Flask(__name__, template_folder='Templates')

@app.route('/')
def index():
    print(request.headers)
    return render_template('TestePorta.html', 
        meuIp = request.headers.get('X-Forwarded-For') or 
        request.headers.get('X-Real-IP') or 
        request.headers.get('Remote-Addr') 
    )
    
def port(endereco,porta):    
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex((endereco,porta))
    sock.close()
    return result == 0

@app.route('/porta', methods=['POST'])
def receberPorta():
    return port(request.form.get('ip'),
                request.form.get('porta'))
    
if __name__ == '__main__':
    app.run(debug=True)

    