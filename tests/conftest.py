import sys
import os
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from database import Database

@pytest.fixture
def client():
    app.config['TESTING'] = True 
    with app.test_client() as client:
        with app.app_context():
            clearMemory()
            yield client

def clearMemory():
    Database.logs.clear()
    Database.knownUsers.clear()
    Database.knownClients.clear()
    Database.knownIps.clear()