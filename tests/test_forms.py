import pytest
from todo_project import app, db
from todo_project.models import User
from todo_project.forms import RegistrationForm, LoginForm, UpdateUserInfoForm, UpdateUserPassword, TaskForm, UpdateTaskForm
from flask_login import current_user

@pytest.fixture
def setup():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        db.create_all()
        user = User(username='existinguser', password='password')
        db.session.add(user)
        db.session.commit()
        yield
        db.session.remove()
        db.drop_all()

@pytest.fixture
def authenticated_user(setup):
    with app.test_request_context():
        user = User.query.filter_by(username='existinguser').first()
        current_user._get_current_object = lambda: user
        yield

def test_registration_form(setup):
    with app.test_request_context():
        form = RegistrationForm(username='uniqueuser', password='password', confirm_password='password')
        assert form.validate() is True

def test_login_form():
    with app.test_request_context():
        form = LoginForm(username='testuser', password='password')
        assert form.validate() is True

def test_update_user_info_form(authenticated_user):
    with app.test_request_context():
        form = UpdateUserInfoForm(username='testuser')
        assert form.validate() is True

def test_update_user_password_form():
    with app.test_request_context():
        form = UpdateUserPassword(old_password='password', new_password='newpassword')
        assert form.validate() is True

def test_task_form():
    with app.test_request_context():
        form = TaskForm(task_name='Test Task')
        assert form.validate() is True

def test_update_task_form():
    with app.test_request_context():
        form = UpdateTaskForm(task_name='Updated Task')
        assert form.validate() is True
