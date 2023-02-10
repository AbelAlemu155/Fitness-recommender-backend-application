
from datetime import datetime

from app import db


class PermanentWater(db.Model):
    __tablename__= 'permanentwaters'
    id = db.Column(db.Integer, primary_key=True)
    #intake in liters
    intake=db.Column(db.Float, default=0)
    logtime = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))