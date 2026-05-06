from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user
from forms.auth_forms import RegisterForm, LoginForm, ChangePasswordForm
from services.auth_service import register_user, authenticate_user, change_password

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('todos.index'))

    form = RegisterForm()
    if form.validate_on_submit():
        user, error = register_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        if error:
            flash(error, 'danger')
        else:
            flash('Registration successful! Please log in.', 'success')
            return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('todos.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user, error = authenticate_user(
            email=form.email.data,
            password=form.password.data,
            remember=form.remember_me.data,
        )
        if error:
            flash(error, 'danger')
        else:
            next_page = request.args.get('next')
            return redirect(next_page or url_for('todos.index'))

    return render_template('auth/login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password_view():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        success, error = change_password(
            user=current_user,
            current_password=form.current_password.data,
            new_password=form.new_password.data,
        )
        if error:
            flash(error, 'danger')
        else:
            flash('Password changed successfully.', 'success')
            return redirect(url_for('todos.index'))

    return render_template('auth/change_password.html', form=form)