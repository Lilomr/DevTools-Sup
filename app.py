import logging

from flask import Flask
from flask_cors import CORS

from api import api as api_blueprint

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
app.register_blueprint(api_blueprint)

if __name__ == "__main__":
    app.run(debug=False)
