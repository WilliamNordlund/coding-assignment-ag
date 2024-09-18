from flask import Blueprint, request, jsonify
from database import Database




log_blueprint = Blueprint('log', __name__)

@log_blueprint.route('', methods=['POST'])
def on_receive_log():
    # LOG FORMAT
    # {
    #   "username": "UserA",
    #   "device_id": "Laptop-999",
    #   "ip_address": "203.0.113.10",
    #   "login_time": "2024-09-17T10:05:00Z"
    # }


    log_data = request.get_json()

    Database.handle_recieve_log(log_data)
    return log_data
