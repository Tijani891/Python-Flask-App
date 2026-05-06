import pytest
from app import create_app
from extensions import db


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


def register_and_login(client):
    client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@test.com',
        'password': 'password123',
        'confirm_password': 'password123',
    }, follow_redirects=True)
    client.post('/auth/login', data={
        'email': 'test@test.com',
        'password': 'password123',
    }, follow_redirects=True)


def test_create_todo(client):
    register_and_login(client)
    response = client.post('/todos/create', data={
        'content': 'Test task',
        'priority': 'medium',
        'status': 'pending',
    }, follow_redirects=True)
    assert response.status_code == 200


def test_todo_index_requires_login(client):
    response = client.get('/todos/', follow_redirects=True)
    assert b'log in' in response.data.lower()


def test_complete_todo(client):
    register_and_login(client)
    client.post('/todos/create', data={
        'content': 'Task to complete',
        'priority': 'high',
        'status': 'pending',
    }, follow_redirects=True)
    response = client.post('/todos/1/complete', follow_redirects=True)
    assert response.status_code == 200


def test_delete_todo(client):
    register_and_login(client)
    client.post('/todos/create', data={
        'content': 'Task to delete',
        'priority': 'low',
        'status': 'pending',
    }, follow_redirects=True)
    response = client.post('/todos/1/delete', follow_redirects=True)
    assert response.status_code == 200


def test_search_todos(client):
    register_and_login(client)
    client.post('/todos/create', data={
        'content': 'Searchable task',
        'priority': 'medium',
        'status': 'pending',
    }, follow_redirects=True)
    response = client.get('/todos/search?q=Searchable')
    assert response.status_code == 200


def test_todo_stats(client):
    register_and_login(client)
    response = client.get('/todos/stats')
    assert response.status_code == 200