from flask import Flask
from routes.risk import risk_blueprint
from routes.log import log_blueprint

app = Flask(__name__)

app.register_blueprint(risk_blueprint, url_prefix='/risk')
app.register_blueprint(log_blueprint, url_prefix='/log')

if __name__ == "__main__":
    app.run(debug=True)