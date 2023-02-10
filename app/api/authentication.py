from datetime import datetime, timedelta, date

from flask import g, jsonify, session, request, url_for
from flask_httpauth import HTTPBasicAuth
from .. import db

from . import api
from ..Plan.Meal import FoodLog
from ..emails import send_email

auth = HTTPBasicAuth()
from ..models import User
from .errors import unauthorized,forbidden
import random

@auth.verify_password
def verify_password(email_or_token,password):
    if request.endpoint=='api.register' or request.endpoint=='api.validator' or request.endpoint =='api.change_password' or request.endpoint =='api.sendemail':
        return True;
    if email_or_token == '':
        return False
    if password=='' :
        g.current_user = User.verify_auth_token(email_or_token)
        g.token_used = True
        return g.current_user is not None
    u=User.query.filter_by(email=email_or_token).first()
    if not u:
        return False
    g.current_user=u
    g.token_used=False
    return u.verify_password(password)


@auth.error_handler
def auth_error():
    return unauthorized('Invalid credentials')


@api.before_request
@auth.login_required
def before_request():
   if request.endpoint !='api.register' and request.endpoint !='api.validator'  and request.endpoint !='api.change_password' and request.endpoint!='api.confirm_by_email' and request.endpoint !='api.is_confirmed' and request.endpoint!='api.sendemail' :
       if not g.current_user.is_anonymous and \
               not g.current_user.confirmed:
           print('unconfirmed')
           return forbidden('Unconfirmed Account')


       date2=g.current_user.remaining_food_time
       date3=g.current_user.remaining_water_time



       if date2.date() != date.today():
           g.current_user.remaining_food_time=datetime.now()
           ilfs=g.current_user.logged_foods.all()
           for lf in ilfs:
               FoodLog.query.filter_by(id=lf.id).delete()

           g.current_user.logged_foods=[]
           g.current_user.logged_food_intake=0
           db.session.add(g.current_user)
           db.session.commit()

       if date3.date() != date.today():
           g.current_user.remaining_water_time = datetime.now()
           g.current_user.logged_water_intake = 0
           db.session.add(g.current_user)
           db.session.commit()









@api.route('/tokens/', methods=['POST'])
def get_token():
    if g.current_user.is_anonymous or g.token_used:
        return unauthorized('Invalid credentials')
    return jsonify({'token': g.current_user.generate_auth_token(
        expiration=3600), 'expiration': 3600})

@api.route('/verify_token')
def verify_token():
    return ''

@api.route('/register', methods=['POST'])
def register():

    u = User.from_json(request.get_json(force=True))
    u.email= u.email.lower()
    db.session.add(u)
    db.session.commit()
    return jsonify(u.to_json()), 201, \
           {'Location': url_for('api.get_user', id=u.id)}



@api.route('/validator', methods=['Post'])
def validator():
    email=request.get_json(force=True).get('email')
    check_email=email.lower()
    email_val=True

    if User.query.filter_by(email=check_email).first():
        email_val=False

    return jsonify({ 'email' : email_val})


@api.route('/isconfirmed/<email>')
def is_confirmed(email):
    u=User.query.filter_by(email=email).first_or_404()
    if u.confirmed:
        return jsonify({'isconfirmed': True})
    return jsonify({'isconfirmed': False})

@api.route('/sendemail', methods=['Post'])
def sendemail():
    email = request.get_json(force=True).get('email')
    u = User.query.filter_by(email=email).first_or_404()
    token = random.randint(1000, 9999)

    token2=str(token)
    print('this is the token ************'+token2)
    send_email(u.email, 'Confirm Your account', '/auth/api/confirm', user=u, token=token)
    return jsonify({'token': token2})


@api.route('/confirm/<email>')
def confirm_by_email(email):
    u=User.query.filter_by(email=email).first_or_404()
    u.confirmed=True
    db.session.add(u)
    db.session.commit()
    return ''



























