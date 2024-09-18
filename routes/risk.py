from flask import Blueprint, request, jsonify

risk_blueprint = Blueprint('risk', __name__)

@risk_blueprint.route('/isuserknown', methods=['GET'])
def is_user_known():
    return jsonify(False)

@risk_blueprint.route('/isipknown', methods=['GET'])
def is_ip_known():
    return jsonify(False)

@risk_blueprint.route('/isclientknown', methods=['GET'])
def is_client_known():
    return jsonify(False)