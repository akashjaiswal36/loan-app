import pytest
from app import app  # replace 'app' with the actual name of your file if it's not app.py
from flask import url_for
import io

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"html" in response.data.lower()  # Rough check that it's HTML

def test_foreclosure_page(client):
    response = client.get('/foreclosure')
    assert response.status_code == 200
    assert b"html" in response.data.lower()

def test_generate_excel(client):
    data = {
        'principal': '100000',
        'rate': '0.12',
        'months': '12'
    }
    response = client.post('/generate', data=data)
    assert response.status_code == 200
    assert response.mimetype == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    assert response.headers['Content-Disposition'].startswith('attachment;')

def test_calculate_foreclosure(client):
    data = {
        'principal': '100000',
        'rate': '0.12',
        'months': '12',
        'foreclose_month': '6'
    }
    response = client.post('/calculate_foreclosure', data=data)
    assert response.status_code == 200
    assert b"Remaining Balance" in response.data or b"remaining_balance" in response.data
