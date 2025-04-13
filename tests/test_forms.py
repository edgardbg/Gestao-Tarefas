import pytest
from todo_project import app, db
from todo_project.models import User
from todo_project.forms import RegistrationForm, LoginForm, UpdateUserInfoForm, UpdateUserPassword, TaskForm, UpdateTaskForm

@pytest.fixture
def setup():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        user = User(username='existinguser', password='password')
        db.session.add(user)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()

def test_registration_form(setup):
    with app.test_request_context():
        form = RegistrationForm(username='uniqueuser', password='password', confirm_password='password')
        assert form.validate() is True

def test_login_form():
    with app.app_context():
        form = LoginForm(username='testuser', password='password')
        assert form.validate() is True

def test_update_user_info_form():
    with app.app_context():
        form = UpdateUserInfoForm(username='testuser')
        assert form.validate() is True

def test_update_user_password_form():
    with app.app_context():
        form = UpdateUserPassword(old_password='password', new_password='newpassword')
        assert form.validate() is True

def test_task_form():
    form = TaskForm(task_name='Test Task')
    assert form.validate() is True

def test_update_task_form():
    form = UpdateTaskForm(task_name='Updated Task')
    assert form.validate() is True
