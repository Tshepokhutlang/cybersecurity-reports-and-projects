import json

from app import app


def test_health_endpoint():
    with app.test_client() as client:
        response = client.get('/api/health')
        assert response.status_code == 200
        assert response.get_json() == {'status': 'healthy'}


def test_detect_requires_subject_and_body():
    with app.test_client() as client:
        response = client.post('/api/detect', json={'email_subject': '', 'email_body': ''})
        assert response.status_code == 400
        assert 'error' in response.get_json()
