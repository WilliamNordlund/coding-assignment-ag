from flask import Blueprint, request, jsonify
from database import Database
risk_blueprint = Blueprint('risk', __name__)

@risk_blueprint.route('/isuserknown', methods=['GET'])
def is_user_known():
    username = request.args.get('username')
    return jsonify(username in Database.knownUsers if username else False)

@risk_blueprint.route('/isipknown', methods=['GET'])
def is_ip_known():
    ip = request.args.get('ip')
    return jsonify(ip in Database.knownIps if ip else False)

@risk_blueprint.route('/isclientknown', methods=['GET'])
def is_client_known():
    client = request.args.get('client')
    return jsonify(client in Database.knownClients if client else False)

@risk_blueprint.route('/LastSuccessfulLoginDate', methods=['GET'])
def last_successful_login_date():
    username = request.args.get('username')
    if username in Database.knownUsers:
        last_success = Database.knownUsers[username]["logins"]["last_success"]
        return jsonify(last_success if last_success else None)
    else:
        return jsonify(None)

@risk_blueprint.route('/LastFailedLoginDate', methods=['GET'])
def last_failed_login_date():
    username = request.args.get('username')
    if username in Database.knownUsers:
        last_fail = Database.knownUsers[username]["logins"]["last_fail"]
        return jsonify(last_fail if last_fail else None)
    else:
        return jsonify(None)

@risk_blueprint.route('/failedlogincountlastweek', methods=['GET'])
def failed_login_count_last_week():
    username = request.args.get('username')
    if username in Database.knownUsers:
        count = Database.failed_logins_last_week(username)
        return jsonify({"failed_login_count": count})
    else:
        return jsonify({"failed_login_count": 0})
