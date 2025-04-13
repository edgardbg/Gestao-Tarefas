import pytest
from todo_project import db
from todo_project.models import User, Task

@pytest.fixture(scope='module')
def setup():
    db.create_all()
    yield
    db.drop_all()

def test_user_model(setup):
    user = User(username='testuser', password='password')
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.username == 'testuser'
    assert user.password == 'password'
    assert user.tasks == []

def test_task_model(setup):
    user = User(username='testuser2', password='password')
    db.session.add(user)
    db.session.commit()

    task = Task(content='Test Task', author=user)
    db.session.add(task)
    db.session.commit()

    assert task.id is not None
    assert task.content == 'Test Task'
    assert task.date_posted is not None
    assert task.user_id == user.id
    assert task.author == user
