from app.trainer.model import *
from ..models import User, Role
from ..Plan.plan import UserPlan
from .. import db
from flask import g, jsonify, session, request, url_for
from app.api import api

# registration handler for trainer
@api.route('/trainer/register', methods=['POST'])
def tregister():

    u = User.from_json(request.get_json(force=True))
    u.role = Role.query.filter_by(name="Trainer").first()
    u.email = u.email.lower()
    db.session.add(u)

    trainer = Trainer.from_json(request.get_json(force=True))
    trainer.id = u.id
    db.session.add(trainer)

    db.session.commit()
    # return jsonify(u.to_json().update(trainer.to_json())), 201, \
    #     {'Location': url_for('api.get_user', id=u.id)}
    returnData = u.to_json()
    # returnData.update(trainer.to_json())
    returnData.update(
        {
            "id": u.id,
            "email": u.email,
            "token": u.generate_auth_token(expiration=3600),
            "expiration": 3600
        }
    )
    return jsonify(returnData), 201, \
        {'Location': url_for('api.get_user', id=u.id)}

# login handler for trainer
@api.route('/trainer/login', methods=['POST'])
def tlogin():
    data = request.get_json()

    u = User.query.filter_by(email=data.get('email')).first()
    if not u:
        return jsonify({'message': 'unknown user'}), 404
    isPassword = u.verify_password(data.get('password'))

    if not isPassword:
        return jsonify({'message': 'incorrect password'}), 404

    if(u.role_id != 2):
        return jsonify({'message': 'trainer only'}), 404

    u.ping()

    returnData = u.to_json()

    returnData.update(
        {
            "id": u.id,
            "email": u.email,
            "token": u.generate_auth_token(expiration=3600),
            "expiration": 3600
        }
    )

    return jsonify(returnData), 200, \
        {'Location': url_for('api.get_user', id=u.id)}

# get a trainer
@api.route('/trainer/<int:id>')
def get_trainer(id):
    trainer = Trainer.query.get_or_404(id)
    return jsonify(trainer.to_json())

# Get the trainer information 
@api.route('/trainer/info/<int:id>')
def get_trainer_info(id):
    trainerClientCount = TrainerClient.query.filter_by(trainer_id=id).count()
    trainerRequestCount = TrainerRequest.query.filter_by(trainer_id=id).count()
    print({'client_count': trainerClientCount,
           'request_count': trainerRequestCount})
    return jsonify({'client_count': trainerClientCount, 'request_count': trainerRequestCount})

#Get clients for a trainer
@api.route('/trainer/<int:id>/clients')
def get_clients(id):
    page = request.args.get('page', 1, type=int)
    trainerClient = TrainerClient.query.filter_by(
        trainer_id=id).paginate(page=page, per_page=5)
    trainerClientCount = TrainerClient.query.filter_by(trainer_id=id).count()

    prev = next = None
    if trainerClient.has_prev:
        prev = url_for('api.get_clients', page=page-1)
    if trainerClient.has_next:
        next = url_for('api.get_clients', page=page+1)

    returnData = {
        "clients": [{"client_id": client.client_id} for client in trainerClient.items],
        "client_count": trainerClientCount,
        "next_url": next,
        "prev_url": prev,
        "page": page,
        "total_pages": trainerClient.total
    }

    return jsonify(returnData)

#Get client requests
@api.route('/trainer/<int:id>/requests')
def get_requests(id):
    page = request.args.get('page', 1, type=int)
    trainerRequest = TrainerRequest.query.filter_by(
        trainer_id=id).paginate(page=page, per_page=5)
    trainerRequestCount = TrainerRequest.query.filter_by(trainer_id=id).count()

    prev = next = None
    if trainerRequest.has_prev:
        prev = url_for('api.get_requests', page=page-1)
    if trainerRequest.has_next:
        next = url_for('api.get_requests', page=page+1)

    returnData = {
        "requests": [{"request_id": request.client_id} for request in trainerRequest.items],
        "request_count": trainerRequestCount,
        "next_url": next,
        "prev_url": prev,
        "page": page
    }

    return jsonify(returnData)

#Get User plan information for client
@api.route('/client/info/<int:id>')
def get_client_info(id):
    client_basic = User.query.get_or_404(id)
    client_info = UserPlan.query.get_or_404(id)
    client_info_tojson = {
        "username": client_basic.username,
        "age": client_info.age,
        "gender": client_info.gender,
        "height": client_info.height,
        "weight": client_info.weight,
        "goal": client_info.goal,
        "goal_weight": client_info.goal_weight,
        "activity_level": client_info.le_activity,
        "fitness_level": client_info.fitness_level,
        "physical_limitation": client_info.physical_limitation,
        "days_workout": client_info.num_of_days_workout,
        "requires_motivation": client_info.requires_motivation,
        "days_goal": client_info.num_of_days_goal,
        "week_goal": client_info.num_of_weeks_goal,
    }
    return jsonify(client_info_tojson), 200

# Get all fitness plans
@api.route('/trainer/<int:id>/fplan')
def get_fitness_plan(id):
    fitness_plan = AssignFitnessPlan.query.filter_by(trainer_id=id).all()
    return jsonify([fp.to_json() for fp in fitness_plan])

# Get fitness plan for one client
@api.route('/trainer/<int:trainer_id>/fplan/<int:client_id>')
def get_client_fitness_plan(trainer_id, client_id):
    fitness_plan = AssignFitnessPlan.query.filter_by(
        trainer_id=trainer_id, client_id=client_id).all()
    return jsonify([fp.to_json() for fp in fitness_plan])

@api.route('/trainer/workout/<int:trainer_id>/<email>')
def get_cfp_email(trainer_id,email):
    u=User.query.filter_by(email=email).first_or_404()
    client_id=u.id
    fitness_plan = AssignFitnessPlan.query.filter_by(
        trainer_id=trainer_id, client_id=client_id).first()
    return jsonify(fitness_plan.to_json())





# Create fitness plan for one client
@api.route('/trainer/fplan', methods=['POST'])
def create_fitness_plan():
    data = request.get_json()

    assign_fp = AssignFitnessPlan.from_json(data)
    db.session.add(assign_fp)
    db.session.flush()
    db.session.refresh(assign_fp)
    
    workoutsJSON = data.get('workouts')
    # print(workoutsJSON)
    for workout in workoutsJSON:
        assign_workout = AssignWorkouts.from_json(workout)
        print("NEW FPLAN:",assign_fp.id)
        assign_workout.fplan_id = assign_fp.id
        db.session.add(assign_workout)
    
    db.session.commit()

    return jsonify(assign_fp.to_json())


@api.route('/trainer/fplan/<int:fplan_id>', methods=['DELETE'])
def delete_fitness_plan(fplan_id):
    fitness_plan = AssignFitnessPlan.query.get_or_404(fplan_id)
    workouts = fitness_plan.workouts
    for workout in workouts:
        db.session.delete(workout)
    
    db.session.delete(fitness_plan)

    
    db.session.commit()
    return jsonify({"message": "fitness plan deleted"})

# Get all diet plans
@api.route('/trainer/<int:id>/dplan')
def get_diet_plan(id):
    diet_plan = AssignDietPlan.query.filter_by(trainer_id=id).all()
    return jsonify([dp.to_json() for dp in diet_plan])

# Get diet plan for one client
@api.route('/trainer/<int:trainer_id>/dplan/<int:client_id>')
def get_client_diet_plan(trainer_id, client_id):
    diet_plan = AssignDietPlan.query.filter_by(
        trainer_id=trainer_id, client_id=client_id).all()
    return jsonify([dp.to_json() for dp in diet_plan])

@api.route('/trainer/diet/<int:trainer_id>/<email>')
def get_cdplan_email(trainer_id,email):
    u=User.query.filter_by(email=email).first_or_404()
    client_id=u.id
    diet_plan = AssignDietPlan.query.filter_by(
        trainer_id=trainer_id, client_id=client_id).first()

    return jsonify(diet_plan.to_json())




# Create diet plan for one client
@api.route('/trainer/dplan', methods=['POST'])
def create_diet_plan():
    data = request.get_json()
    print(data, AssignDietPlan.from_json)
    assign_dp = AssignDietPlan.from_json(jsonData=data)
    db.session.add(assign_dp)
    db.session.flush()
    db.session.refresh(assign_dp)
    
    mealsJSON = data.get('meals')
    print(mealsJSON)
    for meal in mealsJSON:
        assign_meal = AssignFood.from_json(meal)
        print("DPLAN:",assign_dp.id)
        assign_meal.dplan_id = assign_dp.id
        db.session.add(assign_meal)

    db.session.commit()

    return jsonify(assign_dp.to_json())

@api.route('/trainer/dplan/<int:dplan_id>', methods=['DELETE'])
def delete_diet_plan(dplan_id):
    diet_plan = AssignDietPlan.query.get_or_404(dplan_id)
    meals = diet_plan.meals
    for meal in meals:
        db.session.delete(meal)
    
    db.session.delete(diet_plan)
    
    db.session.commit()
    return jsonify({"message": "diet plan deleted"})


#----- Client --------
#search for trainers
@api.route('/search/trainer')
def searchTrainer() :
    page = request.args.get('page', 1, type=int)
    search_params = request.args.get('search', type=str, default="a")
    trainers = Trainer.query.filter(
        Trainer.user.name.like("%" + search_params + "%"),
        Trainer.approve == True
    ).paginate(page, per_page=4)
    #print(trainers.items)
    
    return jsonify({
        "results" : [t.to_json() for t in trainers.items],
    })


@api.route('/clientapproval/<email>/<int:trainer_id>')
def check_client_approval(email,trainer_id):
    u=User.query.filter_by(email=email).first_or_404()
    u_id=u.id
    tclients=TrainerClient.query.filter_by(client_id=u_id,trainer_id=trainer_id).all()
    trequests=TrainerRequest.query.filter_by(client_id=u_id,trainer_id=trainer_id).all()
    if len(tclients) !=0:
        return jsonify({'approval': True,'request': True})

    else:
        if len(trequests) !=0:
            return jsonify({'approval': False,'request': True})
        return jsonify({'approval': False,'request': False})





@api.route('/getapprovedtrainers/')
def get_aprroved_trainers():
    ts=Trainer.query.filter_by(approve=True).all()

    return jsonify([t.to_json() for t in ts])

@api.route('/makerequest/<email>/<int:trainer_id>')
def make_request(email,trainer_id):
    u=User.query.filter_by(email=email).first_or_404()
    tr=TrainerRequest(client_id=u.id,trainer_id=trainer_id)
    db.session.add(tr)
    db.session.commit()
    return ''




