from flask import Flask,render_template,request

app = Flask(__name__, template_folder='Templates')



@app.route('/')
def index():
    print(request.headers)
    return render_template('TestePorta.html', meuIp = request.headers.get('Remote-Addr'))
    




if __name__ == '__main__':
    app.run(debug=True)

    