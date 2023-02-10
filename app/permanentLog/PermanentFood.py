from datetime import datetime

from app import db


class PermanentFood(db.Model):
    __tablename__= 'permanentfoods'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text)
    calories = db.Column(db.FLOAT)
    category = db.Column(db.Integer, default=1)
    logtime = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))






