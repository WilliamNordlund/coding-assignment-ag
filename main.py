from flask import Flask, request

app = Flask(__name__)

@app.route('./log', methods=['POST'])
def on_receive_log():
    log_data = request.get_json()
    return log_data

@app.route('./risk', methods=['GET'])
def on_risk_assessment():
    
    return ""        