from . import auth
from flask import render_template, redirect, flash, request, url_for, session, current_app
from flask_login import login_user, login_required, logout_user,current_user
from .forms import LoginForm,RegistrationForm
from ..models import User
from .. import db
from ..emails import send_email
@auth.route('/login', methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next=request.args.get('next')
            name=user.username
            if next is None or not next.startswith('/'):
                next=url_for('main.index')
                session['name'] = name
            return redirect(next)
        flash('invalid username or password')
    return render_template('auth/login.html',form=form)



@auth.route('/index')
@login_required
def index():
    name=session.get('name')
    return render_template('/auth/index.html', name=name)
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('.index'))

@auth.route('/register', methods=['GET','POST'])
def register():
    form= RegistrationForm()

    if form.validate_on_submit():
        u=User(username=form.username.data, email=form.email.data , password=form.password.data)
        db.session.add(u)
        db.session.commit()
        token=u.generate_confirmation_token(u.id)
        send_email(u.email,'Confim your account','/auth/emails/confirm', user=u, token=token)
        flash(message='Confirmation email has been sent')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html',form=form)

@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have been confirmed')
    else:
        flash('invalid confirmation token or expired token')
    return redirect(url_for('main.index',_external=True))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static' \
            and request.endpoint != 'api':

        return redirect(url_for('auth.unconfirmed'))

@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirm.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    token=current_user.generate_confirmation_token(current_user.id)
    send_email(current_user.email, 'Confirm Your account', '/auth/emails/confirm', user=current_user, token=token)
    flash('Confirmation link has been resent to your email')
    return redirect(url_for('main.index'))