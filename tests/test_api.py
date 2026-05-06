import pytest
import json
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


def test_api_get_todos(client):
    register_and_login(client)
    response = client.get('/api/v1/todos')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'success'


def test_api_create_todo(client):
    register_and_login(client)
    response = client.post('/api/v1/todos',
        data=json.dumps({'content': 'API task', 'priority': 'high'}),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['status'] == 'success'
    assert data['todo']['content'] == 'API task'


def test_api_create_todo_missing_content(client):
    register_and_login(client)
    response = client.post('/api/v1/todos',
        data=json.dumps({'priority': 'high'}),
        content_type='application/json'
    )
    assert response.status_code == 400


def test_api_complete_todo(client):
    register_and_login(client)
    client.post('/api/v1/todos',
        data=json.dumps({'content': 'Task to complete'}),
        content_type='application/json'
    )
    response = client.post('/api/v1/todos/1/complete')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['todo']['status'] == 'completed'


def test_api_delete_todo(client):
    register_and_login(client)
    client.post('/api/v1/todos',
        data=json.dumps({'content': 'Task to delete'}),
        content_type='application/json'
    )
    response = client.delete('/api/v1/todos/1')
    assert response.status_code == 200


def test_api_search_todos(client):
    register_and_login(client)
    client.post('/api/v1/todos',
        data=json.dumps({'content': 'Searchable API task'}),
        content_type='application/json'
    )
    response = client.get('/api/v1/todos/search?q=Searchable')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['count'] >= 1


def test_api_stats(client):
    register_and_login(client)
    response = client.get('/api/v1/stats')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'stats' in data


def test_api_requires_login(client):
    response = client.get('/api/v1/todos')
    assert response.status_code == 302