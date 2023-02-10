from flask import request, url_for, jsonify
from sqlalchemy import or_

from app.Plan import Workout
from app.api import api


@api.route('/searchworkout',methods=['POST'])
def search_workout():
    per_page = 15
    page = request.get_json(force=True).get('page')
    #keyword is name or muscle_target
    keyword = request.get_json(force=True).get('keyword')
    #type is integer, 1,2,4 or combination
    type = request.get_json(force=True).get('type')
    cduration=request.get_json(force=True).get('cduration')
    duration=request.get_json(force=True).get('duration')
    #intensity is an integer, 1,2,4
    intensity=request.get_json(force=True).get('intensity')
    sort=request.get_json(force=True).get('sort')
    ctype=request.get_json(force=True).get('ctype')
    cintensity=request.get_json(force=True).get('cintensity')
    tworkout=TypeWorkout(type2=type)
    iworkout=IntensityWorkout(intensity2=intensity)
    dworkout=DurationWorkout(duration=duration)
    w_query = Workout.query.msearch(keyword)
    if ctype == 1:
        if type == 1:
            w_query = w_query.filter_by(type=1)
        elif type == 2:
            w_query = w_query.filter_by(type=2)
        elif type == 4:
            w_query = w_query.filter_by(type=3)
    elif ctype == 2:
        if tworkout.has_type(1) and tworkout.has_type(2):
            w_query = w_query.filter((Workout.type == 1) | (Workout.type == 2))
        elif tworkout.has_type(1) and tworkout.has_type(4):
            w_query = w_query.filter((Workout.type == 1) | (Workout.type == 3))
        elif tworkout.has_type(2) and tworkout.has_type(4):
            w_query = w_query.filter((Workout.type == 2) | (Workout.type == 3))

    elif ctype == 3:
        w_query = w_query.filter((Workout.type == 1) | (Workout.type == 2) | (Workout.type == 3))

    if cintensity == 1:
        if intensity == 1:
            w_query = w_query.filter_by(intensity=1)
        elif intensity == 2:
            w_query = w_query.filter_by(intensity=2)
        elif intensity == 4:
            w_query = w_query.filter_by(intensity=3)

    elif cintensity == 2:
        if iworkout.has_intensity(1) and iworkout.has_intensity(2):
            w_query = w_query.filter((Workout.intensity == 1) | (Workout.intensity == 2))

        elif iworkout.has_intensity(1) and iworkout.has_intensity(4):
            w_query = w_query.filter((Workout.intensity == 1) | (Workout.intensity == 3))
        elif iworkout.has_intensity(2) and iworkout.has_intensity(4):
            w_query = w_query.filter((Workout.intensity == 2) | (Workout.intensity == 3))

    elif cintensity == 3:
        w_query = w_query.filter((Workout.intensity == 1) | (Workout.intensity == 2) | (Workout.intensity == 3))

    #cduration can be zero
    if cduration==1:
        if duration==1:
            w_query=w_query.filter_by(duration=20)
        elif duration==2:
            w_query = w_query.filter_by(duration=40)
        elif duration==4:
            w_query = w_query.filter_by(duration=60)

    elif cduration==2:
        if dworkout.has_duration(1) and dworkout.has_duration(2):
            w_query = w_query.filter((Workout.duration == 20) | (Workout.duration== 40))
        elif dworkout.has_duration(1) and dworkout.has_duration(4):
            w_query = w_query.filter((Workout.duration == 20) | (Workout.duration == 60))
        elif dworkout.has_duration(2) and dworkout.has_duration(4):
            w_query = w_query.filter((Workout.duration == 40) | (Workout.duration == 60))

    elif cduration==3:
        w_query = w_query.filter((Workout.duration == 40) | (Workout.duration == 60) |  (Workout.duration == 20))

    pagination = w_query.paginate(
        page, per_page=per_page,
        error_out=False)
    workouts = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.search_workout', page=page - 1)
    next = None
    if pagination.has_next:
        next = url_for('api.search_workout', page=page + 1)
    if not sort:

        return jsonify({
            'workouts': [w.to_json() for w in workouts],
            'prev_url': prev,
            'next_url': next,
            'count': pagination.total
        })
    else:
        workouts.sort(key=lambda x: x.met_value)
        return jsonify({
            'workouts': [w.to_json() for w in workouts],
            'prev_url': prev,
            'next_url': next,
            'count': pagination.total
        })


            








class TypeWorkout:
    def __init__(self,type2):
        self.type2=type2

    def has_type(self, ty):
        return self.type2 & ty==ty


class IntensityWorkout:
    def __init__(self, intensity2):
        self.intensity2 = intensity2

    def has_intensity(self, ty):
        return self.intensity2 & ty == ty

class DurationWorkout:
    def __init__(self, duration):
        self.duration = duration

    def has_duration(self, du):
        return self.duration & du == du







