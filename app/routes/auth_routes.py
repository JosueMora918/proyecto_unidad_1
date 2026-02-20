import functools
from flask import Blueprint, render_template, redirect, url_for, flash, session
from app.models.user import User
from app.forms import RegisterForm, LoginForm
from app import db

auth_bp = Blueprint('auth', __name__)


# Decorador personalizado para proteger rutas
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'user_id' not in session:
            flash('Por favor inicia sesión para acceder a esta página.', 'warning')
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Verificar si usuario ya existe
        if User.query.filter_by(email=form.email.data).first():
            flash('El email ya está registrado.', 'danger')
            return redirect(url_for('auth.register'))

        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash(f'¡Bienvenido a la tienda, {new_user.username}!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Has iniciado sesión correctamente.', 'success')
            return redirect(url_for('user.index'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')
    return render_template('login.html', form=form)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('auth.login'))