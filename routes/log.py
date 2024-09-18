from flask import Blueprint, request, jsonify
from database import Database

log_blueprint = Blueprint('log', __name__)

@log_blueprint.route('', methods=['POST'])
def on_receive_log():
    log_data = request.get_json()
    client_ip = request.remote_addr
    
    response_data = {
        "log_data": log_data,
        "client_ip": client_ip
    }

    Database.store_log(response_data)
    return response_data
