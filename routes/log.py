from flask import Blueprint, request, jsonify
from database import Database

log_blueprint = Blueprint('log', __name__)

@log_blueprint.route('', methods=['POST'])
def on_receive_log():
    log_data = request.get_json()

    Database.handle_recieve_log(log_data)
    return log_data
