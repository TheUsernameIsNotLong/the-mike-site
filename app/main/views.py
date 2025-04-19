import os
from PIL import Image
from werkzeug.utils import secure_filename
from flask import current_app, render_template, redirect, url_for, abort, flash
from flask_login import login_required, current_user
from . import main
from .forms import EditProfileForm, EditProfileAdminForm
from .. import db
from ..models import Role, User
from ..decorators import admin_required


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user.html', user=user)


@main.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.about_me = form.about_me.data
        
        file = form.avatar.data
        if file:
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1]
            filename = f'user_{current_user.id}.{ext}'
            filepath = os.path.join(current_app.root_path, 'static/avatars', filename)
            image = Image.open(file)
            image = image.convert("RGB")
            image = image.resize((256,256))
            image.save(filepath)
            current_user.avatar = filename
        
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.', "success")
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', form=form)


@main.route('/edit-profile/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin(id):
    user = User.query.get_or_404(id)
    form = EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.confirmed = form.confirmed.data
        user.role = Role.query.get(form.role.data)
        user.name = form.name.data
        user.about_me = form.about_me.data

        file = form.avatar.data
        if file:
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1]
            filename = f'user_{id}.{ext}'
            filepath = os.path.join(current_app.root_path, 'static/avatars', filename)
            image = Image.open(file)
            image = image.convert("RGB")
            image = image.resize((256,256))
            image.save(filepath)
            current_user.avatar = filename

        db.session.add(user)
        db.session.commit()
        flash('The profile has been updated.', "success")
        return redirect(url_for('.user', username=user.username))
    form.email.data = user.email
    form.username.data = user.username
    form.confirmed.data = user.confirmed
    form.role.data = user.role_id
    form.name.data = user.name
    form.about_me.data = user.about_me
    return render_template('edit_profile.html', form=form, user=user)