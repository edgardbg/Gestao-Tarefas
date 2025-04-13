import pytest
from todo_project.todo_project.forms import RegistrationForm, LoginForm, UpdateUserInfoForm, UpdateUserPassword, TaskForm, UpdateTaskForm

def test_registration_form():
    form = RegistrationForm(username='testuser', password='password', confirm_password='password')
    assert form.validate() is True

def test_login_form():
    form = LoginForm(username='testuser', password='password')
    assert form.validate() is True

def test_update_user_info_form():
    form = UpdateUserInfoForm(username='testuser')
    assert form.validate() is True

def test_update_user_password_form():
    form = UpdateUserPassword(old_password='password', new_password='newpassword')
    assert form.validate() is True

def test_task_form():
    form = TaskForm(task_name='Test Task')
    assert form.validate() is True

def test_update_task_form():
    form = UpdateTaskForm(task_name='Updated Task')
    assert form.validate() is True
