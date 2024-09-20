from database import Database

def test_store_known_entities():
    log_data = {
        "username": "UserE",
        "device_id": "Device123",
        "ip_address": "192.168.1.100",
        "login_time": "2024-09-17T10:05:00Z",
        "action": "login"
    }
    Database.store_known_entities(log_data)

    assert "UserE" in Database.knownUsers
    assert "Device123" in Database.knownClients
    assert "192.168.1.100" in Database.knownIps

def test_failed_logins_last_week():
    Database.knownUsers['UserF'] = {
        "logins": {"last_success": None, "last_fail": None, "failed_logins": ['2024-09-14T10:05:00']}
    }

    assert Database.failed_logins_last_week('UserF') == 1
