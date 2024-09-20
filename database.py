from pydantic import BaseModel, ValidationError
from typing import Any, Dict, List
import ipaddress
from datetime import datetime, timedelta

class LogData(BaseModel):
    username: str
    device_id: str
    ip_address: str
    login_time: str
    action: str 

class Database:
    logs: List[Dict[str, str]] = []
    
    knownClients: Dict[str, List[str]] = {}
    knownUsers: Dict[str, Dict[str, Any]] = {}
    knownIps: Dict[str, str] = {}

    internalIp = ipaddress.ip_network("10.97.2.0/24")

    @staticmethod 
    def store_known_entities(log_data: Dict[str, Any]) -> None:
        username = log_data.get("username")
        device_id = log_data.get("device_id")
        ip_address = log_data.get("ip_address")
        action = log_data.get("action")
        timestamp = log_data.get("login_time")

        if username not in Database.knownUsers:
            Database.knownUsers[username] = {
                "devices": [device_id if device_id else "Unknown Device"],
                "logins": {"last_success": None, "last_fail": None, "failed_logins": []}
            }
        else:
            if device_id and device_id not in Database.knownUsers[username]["devices"]:
                Database.knownUsers[username]["devices"].append(device_id)

        if device_id and device_id not in Database.knownClients:
            Database.knownClients[device_id] = [username]
        elif username and username not in Database.knownClients[device_id]:
            Database.knownClients[device_id].append(username)

        if ip_address:
            ip = ipaddress.ip_address(ip_address)
            if ip_address not in Database.knownIps:
                Database.knownIps[ip_address] = "internal" if ip in Database.internalIp else "external"

        if action == "login":
            Database.update_user_logins(username, success=True, timestamp=timestamp)
        elif action == "failed_login":
            Database.update_user_logins(username, success=False, timestamp=timestamp)

    @staticmethod
    def update_user_logins(username: str, success: bool, timestamp: str) -> None:
        if username not in Database.knownUsers:
            Database.knownUsers[username] = {
                "devices": [],
                "logins": {"last_success": None, "last_fail": None, "failed_logins": []}
            }

        if success:
            Database.knownUsers[username]["logins"]["last_success"] = timestamp
        else:
            Database.update_failed_logins(username, timestamp)

    @staticmethod
    def update_failed_logins(username: str, timestamp: str) -> None:
        Database.knownUsers[username]["logins"]["last_fail"] = timestamp
        Database.knownUsers[username]["logins"]["failed_logins"].append(timestamp)

    @staticmethod
    def failed_logins_last_week(username: str) -> int:
        if username not in Database.knownUsers:
            return 0

        now = datetime.now()
        one_week_ago = now - timedelta(days=7)

        failed_logins = Database.knownUsers[username]["logins"]["failed_logins"]
        recent_failures = [login for login in failed_logins if datetime.fromisoformat(login) > one_week_ago]

        return len(recent_failures)

    @staticmethod
    def validate_log_data(log_data: Dict[str, Any]) -> bool:
        try:
            LogData(**log_data)
            return True
        except ValidationError as e:
            print(f"Validation Error: {e}")
            return False

    @staticmethod
    def handle_recieve_log(log_entry: Dict[str, Any]) -> None:
        if Database.validate_log_data(log_entry):
            Database.logs.append(log_entry)
            Database.store_known_entities(log_entry)

            
        else:
            print("Log entry is invalid but storing it for tracking purposes.")
            Database.logs.append({"invalid_log": log_entry})