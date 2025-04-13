import pytest
from todo_project.todo_project import db
from todo_project.models import User, Task

def test_user_model():
    user = User(username='testuser', password='password')
    db.session.add(user)
    db.session.commit()

    assert user.id is not None
    assert user.username == 'testuser'
    assert user.password == 'password'
    assert user.tasks == []

def test_task_model():
    user = User(username='testuser', password='password')
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
