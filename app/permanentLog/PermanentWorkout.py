

from datetime import datetime

from app import db


class PermanentWorkout(db.Model):
    __tablename__= 'permanentworkouts'
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'))
    calories = db.Column(db.FLOAT)
    #duration in seconds
    duration = db.Column(db.Integer)
    logtime = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('users.id'))
