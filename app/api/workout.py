from flask import request, jsonify

from app.Plan import UserPlan, Workout
from app.api import api
from app.models import User


@api.route('/getcalorieworkout/<email>/<w_id>')
def get_calorie_workout(email,w_id):
    u=User.query.filter_by(email=email).first()
    up=UserPlan.query.get(u.plan_id)
    w=Workout.query.get_or_404(w_id)
    wcal=w.workout_calorie(up.weight)
    return jsonify({'wcal':wcal})

@api.route('/calorieduration',methods=['POST'])
def calorie_duration():
    duration=request.get_json().get('duration')
    email=request.get_json().get('email')
    u = User.query.filter_by(email=email).first_or_404()
    wid = request.get_json().get('wid')
    work = Workout.query.filter_by(id=wid).first_or_404()
    uplan = UserPlan.query.get(u.plan_id)
    dcal=duration/60 * work.met_value * 3.5 * uplan.weight/ 200
    return jsonify({'dcal': dcal})


@api.route('/getworkoutbyId/<int:id>')
def get_workout_id(id):
    w=Workout.query.get_or_404(id)
    return jsonify(w.to_json())
@api.route('/getworkoutlist/',methods=['POST'])
def get_workout_list():
    ids=request.get_json().get('ids')
    wkts=[]
    for i in ids:
        w=Workout.query.get_or_404(i)
        wkts.append(w)

    return jsonify([w1.to_json() for w1 in wkts])



