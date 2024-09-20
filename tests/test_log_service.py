from database import Database

def test_on_receive_log(client):
    log_data = {
        "username": "UserC",
        "device_id": "Laptop123",
        "ip_address": "10.97.2.15",
        "login_time": "2024-09-17T10:05:00Z",
        "action": "login"
    }

    response = client.post('/log', json=log_data)

    assert response.status_code == 200
    assert response.get_json() == log_data

    assert 'UserC' in Database.knownUsers
    assert 'Laptop123' in Database.knownClients
    assert '10.97.2.15' in Database.knownIps

def test_invalid_log_data(client):
    log_data = {
        "username": "UserD"
    }

    response = client.post('/log', json=log_data)

    assert response.status_code == 200
    assert Database.logs[-1]["invalid_log"] == log_data