from database import Database

def test_is_user_known(client):
    Database.knownUsers['UserA'] = {"logins": {"last_success": None, "last_fail": None, "failed_logins": []}}
    response = client.get('/risk/isuserknown?username=UserA')

    assert response.status_code == 200
    assert response.get_json() == True

def test_is_user_unknown(client):
    response = client.get('/risk/isuserknown?username=UnknownUser')

    assert response.status_code == 200
    assert response.get_json() == False

def test_is_ip_known(client):
    Database.knownIps['192.168.1.1'] = 'internal'

    response = client.get('/risk/isipknown?ip=192.168.1.1')

    assert response.status_code == 200
    assert response.get_json() == True

def test_is_ip_unknown(client):
    response = client.get('/risk/isipknown?ip=192.168.1.50')

    assert response.status_code == 200
    assert response.get_json() == False