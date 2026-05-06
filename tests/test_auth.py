import pytest
from app import create_app
from extensions import db
from models.user import User


@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def register_user(client, username='testuser', email='test@test.com', password='password123'):
    return client.post('/auth/register', data={
        'username': username,
        'email': email,
        'password': password,
        'confirm_password': password,
    }, follow_redirects=True)


def login_user(client, email='test@test.com', password='password123'):
    return client.post('/auth/login', data={
        'email': email,
        'password': password,
    }, follow_redirects=True)


def test_register_success(client):
    response = register_user(client)
    assert response.status_code == 200


def test_register_duplicate_email(client):
    register_user(client)
    response = register_user(client, username='other')
    assert b'already registered' in response.data


def test_register_duplicate_username(client):
    register_user(client)
    response = register_user(client, email='other@test.com')
    assert b'already taken' in response.data


def test_login_success(client):
    register_user(client)
    response = login_user(client)
    assert response.status_code == 200


def test_login_wrong_password(client):
    register_user(client)
    response = login_user(client, password='wrongpassword')
    assert b'Incorrect password' in response.data


def test_login_nonexistent_email(client):
    response = login_user(client, email='nobody@test.com')
    assert b'No account found' in response.data


def test_logout(client):
    register_user(client)
    login_user(client)
    response = client.get('/auth/logout', follow_redirects=True)
    assert response.status_code == 200


def test_change_password(client):
    register_user(client)
    login_user(client)
    response = client.post('/auth/change-password', data={
        'current_password': 'password123',
        'new_password': 'newpassword123',
        'confirm_password': 'newpassword123',
    }, follow_redirects=True)
    assert response.status_code == 200