import pytest
from todo_project import app, db, bcrypt
from todo_project.models import User, Task
from todo_project.forms import (LoginForm, RegistrationForm, UpdateUserInfoForm, 
                                UpdateUserPassword, TaskForm, UpdateTaskForm)

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client

def test_about(client):
    response = client.get('/about')
    assert response.status_code == 200
    assert b'This Project is developed by' in response.data

def test_login(client):
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    response = client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Login Successfull' in response.data

def test_register(client):
    response = client.post('/register', data=dict(
        username='newuser',
        password='password',
        confirm_password='password'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Account Created For newuser' in response.data

def test_add_task(client):
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    response = client.post('/add_task', data=dict(
        task_name='Test Task'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Task Created' in response.data

def test_all_tasks(client):
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    client.post('/add_task', data=dict(
        task_name='Test Task'
    ), follow_redirects=True)

    response = client.get('/all_tasks')
    assert response.status_code == 200
    assert b'Test Task' in response.data

def test_update_task(client):
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    client.post('/add_task', data=dict(
        task_name='Test Task'
    ), follow_redirects=True)

    task = Task.query.filter_by(content='Test Task').first()

    response = client.post(f'/all_tasks/{task.id}/update_task', data=dict(
        task_name='Updated Task'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Task Updated' in response.data

def test_delete_task(client):
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    client.post('/add_task', data=dict(
        task_name='Test Task'
    ), follow_redirects=True)

    task = Task.query.filter_by(content='Test Task').first()

    response = client.get(f'/all_tasks/{task.id}/delete_task', follow_redirects=True)

    assert response.status_code == 200
    assert b'Task Deleted' in response.data

def test_account(client):
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    client.post('/login', data=dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    response = client.get('/account')
    assert response.status_code == 200
    assert b'Account Settings' in response.data

def test_change_password(client):
    hashed_password = bcrypt.generate_password_hash('password').decode('utf-8')
    user = User(username='testuser', password=hashed_password)
    db.session.add(user)
    db.session.commit()

    client.post('/login', data.dict(
        username='testuser',
        password='password'
    ), follow_redirects=True)

    response = client.post('/account/change_password', data=dict(
        old_password='password',
        new_password='newpassword'
    ), follow_redirects=True)

    assert response.status_code == 200
    assert b'Password Changed Successfully' in response.data
