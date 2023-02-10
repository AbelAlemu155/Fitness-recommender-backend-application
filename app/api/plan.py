from flask import request, jsonify, url_for

from app import db
from app.Plan import UserPlan, WorkoutPlan, Exercise, Workout, Breakfast, Lunch, Dinner, Snack
from app.api import api
from app.models import User


@api.route('/userplan',methods=['POST'])
def create_user_plan():
    email=request.get_json().get('email')
    u=User.query.filter_by(email=email).first()
    uplan=UserPlan.from_json(request.get_json(),u)
    db.session.add(uplan)
    db.session.commit()
    uplan.create_user_plan(u)
    WorkoutPlan.create_workout_plan(u, uplan)


    return ''

@api.route('/exercises/<int:id>')
def get_exercise(id):
    ex=Exercise.query.filter_by(id=id).first_or_404()
    return jsonify(ex.to_json())


@api.route('/workouts/<int:id>')
def get_workout(id):
    wkt=Workout.query.filter_by(id=id).first_or_404()
    return jsonify(wkt.to_json())

@api.route('/workoutex/<int:id>')
def get_workoutex(id):
    wkt = Workout.query.filter_by(id=id).first_or_404()
    exs=wkt.exercises.all()
    return jsonify([ex.to_json() for ex in exs])


@api.route('/workouts/',methods=['POST'])
def get_workouts():
    page=request.get_json().get('page')
    pagination=Workout.query.paginate(page,per_page=15,error_out=False)
    wkts=pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_workouts', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.get_workouts', page=page + 1)

    return jsonify({'prev_url': prev,'next_url': next, 'count': pagination.total,'wkts':[w.to_json() for w in wkts]})


@api.route('/getfoods/',methods=['POST'])
def get_foods():
    page = request.args.get('page', 1, type=int)

    bpag=Breakfast.query.paginate(page,per_page=2,error_out=False)
    bs = bpag.items
    prevb = None
    if bpag.has_prev:
        prevb = url_for('api.get_foods', page=page - 1)
    nextb = None
    if bpag.has_next:
        nextb = url_for('api.get_foods', page=page + 1)

    lpag = Lunch.query.paginate(page, per_page=2, error_out=False)
    ls = lpag.items
    prevl = None
    if lpag.has_prev:
        prevl = url_for('api.get_foods', page=page - 1)
    nextl = None
    if lpag.has_next:
        nextl = url_for('api.get_foods', page=page + 1)

    dpag = Dinner.query.paginate(page, per_page=2, error_out=False)
    ds = dpag.items
    prevd = None
    if dpag.has_prev:
        prevd = url_for('api.get_foods', page=page - 1)
    nextd = None
    if dpag.has_next:
        nextd = url_for('api.get_foods', page=page + 1)

    spag = Snack.query.paginate(page, per_page=5, error_out=False)
    ss = spag.items
    prevs = None
    if spag.has_prev:
        prevs = url_for('api.get_foods', page=page - 1)
    nexts = None
    if spag.has_next:
        nexts = url_for('api.get_foods', page=page + 1)

    return jsonify({'breakfast':[ b.to_json() for b in bs],'lunch': [l.to_json() for l in ls],'dinner': [d.to_json() for d in ds],
                    'snack':[s.to_json() for s in ss],'nextb': nextb,'prevb': prevb,'nextl': nextl,'prevl': prevl,'prevd':prevd
                    ,'nextd': nextd,'prevs': prevs,'nexts': nexts
                    })

@api.route('/getfoodbid/<int:id>')
def get_foodb_id(id):
    food=Breakfast.query.get_or_404(id)
    return jsonify(food.to_json())

@api.route('/getfoodlid/<int:id>')
def get_foodl_id(id):
    food=Lunch.query.get_or_404(id)
    return jsonify(food.to_json())

@api.route('/getfooddid/<int:id>')
def get_foodd_id(id):
    food=Dinner.query.get_or_404(id)
    return jsonify(food.to_json())

@api.route('/getfoodsid/<int:id>')
def get_foods_id(id):
    food=Snack.query.get_or_404(id)
    return jsonify(food.to_json())







@api.route('/userworkouts/<email>')
def get_user_workouts(email):
    u=User.query.filter_by(email=email).first_or_404()
    wktplans=u.workout_plans.all()


    return jsonify([w.to_json() for w in wktplans])

@api.route('/userworkoutplans/<email>')
def get_user_workoutplans(email):
    u = User.query.filter_by(email=email).first_or_404()
    wktplans=u.workout_plans.all()


    return jsonify([pl.to_json() for pl in wktplans])

@api.route('/foodandwater/<email>')
def get_food_and_water(email):
    u = User.query.filter_by(email=email).first_or_404()
    up=UserPlan.query.get(u.plan_id)
    wrintake=up.recommended_water_intake()
    return jsonify({'rwater':wrintake,'water':u.logged_water_intake,'food':u.logged_food_intake,'rfood':u.daily_calorie_intake})





@api.route('/workoutplans/<int:id>')
def get_workout_plan(id):
    wplan=WorkoutPlan.query.filter_by(id=id).first_or_404()
    return jsonify(wplan.to_json())

@api.route('/getplanworkouts/<int:id>')
def get_plan_workouts(id):
    wplan = WorkoutPlan.query.filter_by(id=id).first_or_404()
    wkts=wplan.workouts.all()
    return jsonify([w.to_json() for w in wkts])


@api.route('/getnumweeks/<email>')
def get_weeks(email):
    u = User.query.filter_by(email=email).first_or_404()
    up = UserPlan.query.get(u.plan_id)
    return jsonify({'num':up.num_of_weeks_goal})







@api.route('/getusermealplan/',methods=['POST'] )
def get_user_meal_plan():
    email=request.get_json().get('email')
    page=request.get_json().get('page')


    u=User.query.filter_by(email=email).first_or_404()
    plan=UserPlan.query.get(u.plan_id)
    days=plan.num_of_weeks_goal*7
    allplans=u.meal_plans.all()
    page2= page % len(allplans)
    mp=allplans[page2]

    flist=[]

    b=Breakfast.query.get(mp.breakfast_id)
    l=Lunch.query.get(mp.lunch_id)
    d=Dinner.query.get(mp.dinner_id)
    s=Snack.query.get(mp.snack_id)
    ls=[b.to_json(),l.to_json(),d.to_json(),s.to_json()]



    return jsonify(ls)



@api.route('/userdata/<email>')
def get_data(email):
    email2 = email.replace('%40', '@')
    u=User.query.filter_by(email=email2).first_or_404()
    up=UserPlan.query.filter_by(id=u.plan_id).first_or_404()
    return jsonify(up.to_json())


@api.route('/weeklycaloriegoal/<email>')
def get_calorie_goal(email):
    u = User.query.filter_by(email=email).first_or_404()
    up=UserPlan.query.get(u.plan_id)
    goal=up.calorie_loss_by_exercise()
    return jsonify({'goal':  goal})














