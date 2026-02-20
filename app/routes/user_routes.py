from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app.forms import EditUserForm
from app import db
from .auth_routes import login_required  # Importamos el decorador

user_bp = Blueprint('user', __name__)


@user_bp.route('/')
def index():
    users = User.query.all()
    return render_template('user_list.html', users=users)


@user_bp.route('/profile/<int:id>')
@login_required
def profile(id):
    user = User.query.get_or_404(id)
    return render_template('profile.html', user=user)


@user_bp.route('/profile/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_profile(id):
    user = User.query.get_or_404(id)
    form = EditUserForm(obj=user)  # Pre-carga datos del usuario en el form

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        db.session.commit()
        flash('Perfil actualizado con éxito.', 'success')
        return redirect(url_for('user.profile', id=user.id))

    return render_template('edit_profile.html', form=form, user=user)


@user_bp.route('/profile/<int:id>/delete', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash('El usuario ha sido eliminado.', 'warning')
    return redirect(url_for('user.index'))