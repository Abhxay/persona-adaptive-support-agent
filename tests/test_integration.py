import pytest
import requests

API_URL = 'http://localhost:5000/api'

# Sample test cases for API integration testing

def test_get_endpoint():
    response = requests.get(f"{API_URL}/endpoint")
    assert response.status_code == 200
    assert "data" in response.json()


def test_post_endpoint():
    payload = {'key': 'value'}
    response = requests.post(f"{API_URL}/endpoint", json=payload)
    assert response.status_code == 201
    assert response.json()['key'] == 'value'


def test_put_endpoint():
    payload = {'key': 'updated_value'}
    response = requests.put(f"{API_URL}/endpoint/1", json=payload)
    assert response.status_code == 200
    assert response.json()['key'] == 'updated_value'


def test_delete_endpoint():
    response = requests.delete(f"{API_URL}/endpoint/1")
    assert response.status_code == 204
