from datetime import datetime, date
import datetime
from flask import request, jsonify

from app import db
from app.Plan import Workout, UserPlan
from app.Plan.Meal import FoodLog
from app.api import api
from app.models import User
from app.permanentLog.PermanentFood import PermanentFood
from app.permanentLog.PermanentWater import PermanentWater
from app.permanentLog.PermanentWorkout import PermanentWorkout


@api.route('/updatefoodintake',methods=['POST'])
def update_food():
    food_intake=request.get_json().get('calories')
    name = request.get_json().get('name')
    category = request.get_json().get('category')
    email = request.get_json().get('email')
    u=User.query.filter_by(email=email).first_or_404()
    flog=FoodLog(name=name,calories=food_intake,category=category,user_id=u.id)
    ilfs=u.logged_foods.all()
    u.logged_foods=ilfs + [flog]
    u.logged_food_intake=u.logged_food_intake + food_intake
    plog=PermanentFood(name=name, calories=food_intake,category=category,user_id=u.id)

    db.session.add_all([u,flog,plog])
    db.session.commit()
    return ''

@api.route('/drinkwater',methods=['POST'])
def drink_water():
    water_intake=request.get_json().get('water')
    email = request.get_json().get('email')
    u = User.query.filter_by(email=email).first_or_404()
    u.logged_water_intake=water_intake
    pwater=PermanentWater(intake=water_intake,user_id=u.id)

    db.session.add_all([u,pwater])
    db.session.commit()
    return ''

@api.route('/performworkout',methods=['POST'])
def perform_workout():
    effort=request.get_json().get('effort')
    email = request.get_json().get('email')
    u = User.query.filter_by(email=email).first_or_404()
    #duration in seconds and integer
    duration =request.get_json().get('duration')
    wid=request.get_json().get('wid')
    work=Workout.query.filter_by(id=wid).first_or_404()
    uplan=UserPlan.query.get(u.plan_id)
    calorie=duration/60 * work.met_value * 3.5 * uplan.weight/ 200
    calories=calorie * effort
    pw=PermanentWorkout(duration=duration,workout_id=wid,calories=calories,user_id=u.id)
    db.session.add(pw)
    db.session.commit()
    return ''










@api.route('/getLoggedFoods/<email>')
def get_logged_food(email):
    u=User.query.filter_by(email=email).first_or_404()
    lfoods=u.logged_foods.all()
    return jsonify([l.to_json() for l in lfoods])


@api.route('/getFoodProgress/<email>')
def getFoodProgress(email):
    u = User.query.filter_by(email=email).first_or_404()
    today=date.today()
    weekdays=[today + datetime.timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
    pfoods=u.permanent_foods.all()
    cals=[0 for i in range(len(weekdays))]
    for i in range(len(weekdays)):
        for j in range(len(pfoods)):
            if pfoods[j].logtime.date() != weekdays[i]:
                continue
            else:
                cals[i]=pfoods[j].calories + cals[i]

    reccal=u.daily_calorie_intake


    return jsonify({'cals': cals,'reccal': reccal})


@api.route('/getWaterProgress/<email>')
def getWaterProgress(email):
    u = User.query.filter_by(email=email).first_or_404()
    today = date.today()
    weekdays = [today + datetime.timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
    pwaters=u.permanent_water.all()
    intakes = [0 for i in range(len(weekdays))]
    for i in range(len(weekdays)):
        for j in range(len(pwaters)):
            if pwaters[j].logtime.date() != weekdays[i]:
                continue
            else:
                intakes[i]=pwaters[j].intake + intakes[i]

    up = UserPlan.query.get(u.plan_id)
    recintake = up.recommended_water_intake()



    return jsonify({'intakes': intakes,'recintake': recintake})


@api.route('/getWorkoutProgress/<email>')
def getWorkoutProgress(email):
    u = User.query.filter_by(email=email).first_or_404()
    today = date.today()
    weekdays = [today + datetime.timedelta(days=i) for i in range(0 - today.weekday(), 7 - today.weekday())]
    pwkts=u.permanent_workout.all()
    wcals = [0 for i in range(len(weekdays))]
    for i in range(len(weekdays)):
        for j in range(len(pwkts)):
            if pwkts[j].logtime.date() != weekdays[i]:
                continue
            else:
                wcals[i]=pwkts[j].calories + wcals[i]

    uplan=UserPlan.query.get(u.plan_id)
    reccal=uplan.calorie_loss_by_exercise()


    return jsonify({'wcals': wcals,'reccal': reccal})

















