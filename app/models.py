from datetime import datetime,timedelta

from . import db,login_manager
from . import login_manager
from flask import current_app, url_for
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from markdown import markdown
import bleach
from .exceptions import ValidationError
from app.Plan import UserPlan








class User(UserMixin, db.Model):
    dt= datetime.now() + timedelta(days=1)
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), unique=True, index=True)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    password_hash=db.Column(db.String(128))
    confirmed=db.Column(db.BOOLEAN, default=False)
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    meal_plans = db.relationship('MealPlan', backref='user', lazy='dynamic')
    plan_id=db.Column(db.Integer,db.ForeignKey('plans.id'))
    workout_plans=db.relationship('WorkoutPlan', backref='user', lazy='dynamic')
    daily_calorie_intake=db.Column(db.Integer,index=True,default=0)
    logged_food_intake=db.Column(db.Float,default=0)
    remaining_food_time = db.Column(db.DateTime(), default=dt)
    logged_water_intake=db.Column(db.Float,default=0)
    remaining_water_time = db.Column(db.DateTime(), default=dt)
    logged_foods = db.relationship('FoodLog', backref='user', lazy='dynamic')
    permanent_foods = db.relationship('PermanentFood', backref='user', lazy='dynamic')
    permanent_water = db.relationship('PermanentWater', backref='user', lazy='dynamic')
    permanent_workout = db.relationship('PermanentWorkout', backref='user', lazy='dynamic')
   # comments = db.relationship('Comment', backref='user', lazy='dynamic')
    image_url = db.Column(db.Text,default='https://t3.ftcdn.net/jpg/03/46/83/96/360_F_346839683_6nAPzbhpSkIpb8pmAwufkC7c5eD7wYws.jpg')






    @property
    def password(self):
        raise AttributeError('Password cannot be accessed')


    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def generate_confirmation_token(self,data):
        s=Serializer(current_app.config['SECRET_KEY'],expires_in=3600)
        return s.dumps({'confirm': self.id}).decode('utf-8')


    def confirm(self,token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token.encode('utf-8'))
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed=True
        db.session.add(self)
        return True
    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        db.session.commit()



    def __repr__(self):
        return '<user is: %r>' % self.username

    def __init__(self,**kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(name='Administrator').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    def can(self, permission):
        return self.role is not None and self.role.has_permission(permission)
    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def generate_auth_token(self, expiration):
        s = Serializer(current_app.config['SECRET_KEY'],
                       expires_in=expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        return User.query.get(data['id'])

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user_by_email', email=self.email),
            'username': self.username,
            'member_since': self.member_since,
            'last_seen': self.last_seen,
            'posts_url': url_for('api.get_user_posts', email=self.email),
            'post_count': self.posts.count(),
            'role': self.role.name,
            'image_url': self.image_url
        }
        return json_user
    @staticmethod
    def from_json(json_user):
        name = json_user.get('username')
        password=json_user.get('password')
        email=json_user.get('email')
        return User(name=json_user['username'],password=json_user['password'], email=json_user['email'])









class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
       return False
    def is_administrator(self):
       return False

login_manager.anonymous_user=AnonymousUser


class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(64), unique=True)
    default=db.Column(db.BOOLEAN,default=False,index=True)
    permissions=db.Column(db.Integer)
    users=db.relationship('User', backref='role',lazy='dynamic')


    def __repr__(self):
        return '<Role is: %r>' % self.name

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = 0

    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions += perm

    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions-=perm

    def reset_permissions(self):
        self.permissions=0

    def has_permission(self,perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles={ 'User': [Permission.FOLLOW,Permission.COMMENT, Permission.WRITE],

                'Trainer': [Permission.FOLLOW,Permission.COMMENT, Permission.WRITE,Permission.TRAIN],
                'Administrator':[Permission.FOLLOW,Permission.COMMENT, Permission.WRITE, Permission.ADMIN]



                    }
        default_role='User'
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default= default_role==role.name
            db.session.add(role)
        db.session.commit()



class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(30))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    body_html = db.Column(db.Text)

    #comments = db.relationship('Comment', backref='postu', lazy='dynamic')
    image_url=db.Column(db.Text)

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                        'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(bleach.clean(
            markdown(value, output_format='html'),
            tags=allowed_tags, strip=True))


    def to_json(self):

        json_post = {
            'url': url_for('api.get_post', id=self.id),
            'body': self.body,
            'body_html': self.body_html,
            'timestamp': str(self.timestamp),
            'author_url': url_for('api.get_user_by_email', email=self.author.email),
            'image_url' : self.image_url,
            'title': self.title


        }
        return json_post

    @staticmethod
    def from_json(json_post):
        body = json_post.get('body')
        if body is None or body == '':
            raise ValidationError('post does not have a body')
        return Post(body=body)


db.event.listen(Post.body, 'set', Post.on_changed_body)

class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    TRAIN = 8
    ADMIN = 16






@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


