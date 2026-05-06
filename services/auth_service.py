from extensions import db
from models.user import User
from flask_login import login_user, logout_user
from flask import flash


def register_user(username, email, password):
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return None, "Email already registered"

    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return None, "Username already taken"

    user = User(username=username, email=email)
    user.set_password(password)

    try:
        db.session.add(user)
        db.session.commit()
        return user, None
    except Exception as e:
        db.session.rollback()
        return None, f"Registration failed: {str(e)}"


def authenticate_user(email, password, remember=False):
    user = User.query.filter_by(email=email).first()

    if not user:
        return None, "No account found with that email"

    if not user.check_password(password):
        return None, "Incorrect password"

    if not user.is_active:
        return None, "Account is deactivated"

    login_user(user, remember=remember)
    return user, None


def deactivate_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return False, "User not found"

    user.is_active = False
    try:
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)


def change_password(user, current_password, new_password):
    if not user.check_password(current_password):
        return False, "Current password is incorrect"

    user.set_password(new_password)
    try:
        db.session.commit()
        return True, None
    except Exception as e:
        db.session.rollback()
        return False, str(e)