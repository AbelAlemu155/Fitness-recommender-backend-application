from flask import jsonify, abort, request

from app import db
from app.api import api

from app.api.decorators import permission_required
from app.models import User, Permission, Role


@api.route('/users/')
def get_users():
    users = User.query.all()
    return jsonify({'users': [user.to_json() for user in users]})


@api.route('/user/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/user/<email>')
def get_user_by_email(email):
    email2 = email.replace('%40', '@')
    user = User.query.filter_by(email=email2).first_or_404()
    return jsonify(user.to_json())


@api.route('/user/url/<email>')
def get_user_url(email):
    user = User.query.filter_by(email=email).first_or_404()
    return jsonify({'id': user.id})


@api.route('/change/user/<email>',methods=['PUT'])
def change_password(email):
    user = User.query.filter_by(email=email).first_or_404()
    password= request.get_json().get('password')
    user.password=password
    db.session.add(user)
    db.session.commit()
    return ''

@api.route('/updateTotrainer/<email>',methods=['PUT'])
@permission_required(Permission.ADMIN)
def update_user(email):
    user = User.query.filter_by(email=email).first_or_404()
    role=Role.query.filter_by(name='Trainer').first()
    user.role=role
    db.session.add(user)
    db.session.commit()
    return ''
