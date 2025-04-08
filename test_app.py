import pytest
import sqlite3
from app import app, init_db

@pytest.fixture
def client():
    # Create a test client and initialize the database
    init_db()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'All Feedback' in response.data

def test_submit_feedback(client):
    response = client.post('/submit', data={
        'name': 'Test User',
        'message': 'This is a test message.'
    }, follow_redirects=True)
    
    assert response.status_code == 200
    assert b'Test User' in response.data
    assert b'This is a test message.' in response.data

