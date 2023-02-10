import itertools
import math
from random import random

from flask import url_for
from sqlalchemy import text

from app import db
from app.Plan import MealPlan

from . import Goal



workout_to_exercise = db.Table('workout_exercises',
 db.Column('exercise_id', db.Integer, db.ForeignKey('exercises.id')),
 db.Column('workout_id', db.Integer, db.ForeignKey('workouts.id'))
)

workout_to_plan=db.Table('workout_to_plans',
 db.Column('workout_plan_id', db.Integer, db.ForeignKey('workoutplans.id')),
 db.Column('workout_id', db.Integer, db.ForeignKey('workouts.id'))
)



class Exercise(db.Model):
    __tablename__='exercises'
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(30))
    description=db.Column(db.Text)
    equipment=db.Column(db.String(30))

    duration=db.Column(db.Integer)

    image_url=db.Column(db.Text)

    def to_json(self):
        json_exercise={
            'url' : url_for('api.get_exercise',id=self.id),
            'name': self.name,
            'description': self.description,
            'equipment':self.equipment,
            'duration': self.duration,

            'image_url': self.image_url
        }
        return json_exercise



class Workout(db.Model):
    __tablename__='workouts'
    __searchable__ = ['name', 'muscle_target']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    description = db.Column(db.Text)
    duration=db.Column(db.Integer)
    muscle_target = db.Column(db.String(30))
    type=db.Column(db.Integer)
    intensity=db.Column(db.Integer)
    exercises = db.relationship('Exercise',secondary=workout_to_exercise,backref=db.backref('workouts', lazy='dynamic'),lazy='dynamic')
    met_value=db.Column(db.Float)
    image_url = db.Column(db.Text)
    des='Types of exercise can also be classified as dynamic or static. ' \
        ' exercises such as steady running, tend to produce a lowering of the diastolic blood pressure during ' \
        'exercise, due to the improved blood flow. Conversely, static exercise (such as weight-lifting) ' \
                                                                                'can cause the systolic pressure to rise ' \
        'significantly, albeit transiently, during the performance of the exercise'


    def to_json(self):
        json_workout = {
            'url' : url_for('api.get_workout',id=self.id),
            'name': self.name,
            'description': self.description,
             'duration' : self.duration,
            'muscle_target': self.muscle_target,
            'type': self.type,
            'intensity': self.intensity,
            'met_value':self.met_value,
            'exercises': url_for('api.get_workoutex',id=self.id),
            'image_url': self.image_url
        }
        return  json_workout

    def workout_calorie(self,weight):
        wcal = float(self.duration) * self.met_value * 3.5 * weight / 200
        return wcal












def calculate_calorie_tuple(workouts,weight):

    sum=0
    if len(workouts) ==0:
        return 0



    ls=[9,16,22,27,31]
    for work in workouts:
        wcal=float(work.duration) * work.met_value * 3.5 * weight/200

        sum=sum+ wcal

    return sum

class WorkoutPlan(db.Model):
    __tablename__='workoutplans'
    id = db.Column(db.Integer, primary_key=True)
    week=db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    workouts= db.relationship('Workout',secondary=workout_to_plan,backref=db.backref('workoutplans', lazy='dynamic'),lazy='dynamic')

    def to_json(self):
        json_wplan={
            'url':url_for('api.get_workout_plan',id=self.id),
            'week':self.week,
            'workouts': url_for('api.get_plan_workouts',id=self.id)

        }
        return json_wplan

    @staticmethod
    def create_workout_plan(user,plan):

        if len(user.workout_plans.all()):
            wplan=user.workout_plans.all()
            idlist=[]
            for w in wplan:
                idlist.append(w.id)
                WorkoutPlan.query.filter_by(id=w.id).delete()

            db.session.commit()
            count=0
            for i in idlist:
                str='SELECT COUNT(*) FROM workout_to_plans WHERE workout_plan_id={}'
                str2=str.format(i)
                result = db.engine.execute(str2)
                result2=[row[0] for row in result]
                count=count + result2[0]
            if count !=0:
                for i in idlist:
                    str='DELETE FROM workout_to_plans WHERE workout_plan_id={}'
                    str2 = str.format(i)
                    result = db.engine.execute(str2)











        #getting the user plan information
        plan_id= plan.id

        num_days_workout=plan.num_of_days_workout
        goal=plan.goal
        fitness_level=plan.fitness_level
        num_weeks=plan.num_of_weeks_goal


        #to get the weekly recommended calorie burn by exercise
        calorie_burn_exercise = plan.calorie_loss_by_exercise()




        #querying the workout model for all possiblities
        low_intensities_endurance=Workout.query.filter(Workout.type==Type.ENDURANCETRAINING)\
            .filter_by(intensity=Intensity.LOWINTENSITY).all()
        low_intensities_resistance = Workout.query.filter(Workout.type == Type.RESISTANCETRAINING) \
            .filter_by(intensity=Intensity.LOWINTENSITY).all()

        moderate_intensities_endurance=Workout.query.filter(Workout.type==Type.ENDURANCETRAINING) \
            .filter_by(intensity=Intensity.MODERATEINTENSITY).all()
        moderate_intensities_resistance = Workout.query.filter(Workout.type == Type.RESISTANCETRAINING) \
            .filter_by(intensity=Intensity.MODERATEINTENSITY).all()

        high_intensities_endurance=Workout.query.filter(Workout.type==Type.ENDURANCETRAINING) \
            .filter_by(intensity=Intensity.HIGHINTENSITY).all()
        high_intensities_resistance = Workout.query.filter(Workout.type == Type.RESISTANCETRAINING) \
            .filter_by(intensity=Intensity.HIGHINTENSITY).all()




        counter_list=[[0,0,0],[0,0,0]]
        if goal==Goal.WEIGHTLOSS :
            endurance_ratio=0.75
            resistance_ratio=0.25
        elif goal==Goal.MAINTAININGWEIGHT:
            endurance_ratio=0.5
            resistance_ratio=0.5
        else:
            endurance_ratio=0.25
            resistance_ratio=0.75
        endurance_low=0
        endurance_moderate=0
        endurance_high=0
        resistance_low=0
        resistance_moderate=0
        resistance_high=0


        endurance_num = endurance_ratio * num_days_workout
        resistance_num = resistance_ratio * num_days_workout
        fractionalE, wholeE = math.modf(endurance_num)
        fractionalR, wholeR = math.modf(resistance_num)
        if endurance_ratio != 0.5:
            if fractionalE !=0:
                if fractionalE > 0.5:
                    endurance_num=wholeE + 1
                    resistance_num=wholeR
                elif fractionalR > 0.5:
                    endurance_num=wholeE
                    resistance_num=wholeR + 1
                elif fractionalR== 0.5:
                    if endurance_num > resistance_num:
                        endurance_num=wholeE + 1
                        resistance_num= wholeR
                    else:
                        endurance_num = wholeE
                        resistance_num = wholeR + 1
        elif endurance_ratio == 0.5:
            choices=[0,1]
            if fractionalR !=0:
                choice=random.choice(choices)
                if choice== 0:
                    endurance_num=fractionalE +1
                    resistance_num=fractionalR
                else:
                    endurance_num = fractionalE
                    resistance_num = fractionalR + 1


        endurance_low_num=0
        endurance_moderate_num=0
        endurance_high_num=0
        resistance_low_num=0
        resistance_moderate_num=0
        resistance_high_num=0

        if fitness_level==FitnessLevel.NEVEREXERCISED:
            endurance_low_num=endurance_num
            resistance_low_num=resistance_num

        elif fitness_level==FitnessLevel.BEGINNER:
            endurance_low_num=0.75*endurance_num
            endurance_moderate_num=0.25*endurance_num
            fractionalEl, wholeEl = math.modf(endurance_low_num)
            fractionalEm, wholeEm = math.modf(endurance_moderate_num)
            if fractionalEl > 0.5:
                endurance_low_num = wholeEl + 1
                endurance_moderate_num = wholeEm
            elif fractionalEm > 0.5:
                endurance_low_num = wholeEl
                endurance_moderate_num = wholeEm + 1
            elif fractionalEl == 0.5:
                if endurance_low_num > endurance_moderate_num:
                    endurance_low_num = wholeEl + 1
                    endurance_moderate_num = wholeEm
                else:
                    endurance_low_num = wholeEl
                    endurance_moderate_num = wholeEm + 1

            resistance_low_num=0.75*resistance_num
            resistance_moderate_num=0.25*resistance_num
            fractionalRl, wholeRl = math.modf(resistance_low_num)
            fractionalRm, wholeRm = math.modf(resistance_moderate_num)
            if fractionalRl > 0.5:
                resistance_low_num = wholeRl + 1
                resistance_moderate_num = wholeRm
            elif fractionalRm > 0.5:
                resistance_low_num = wholeRl
                resistance_moderate_num = wholeRm + 1
            elif fractionalRl == 0.5:
                if resistance_low_num > resistance_moderate_num:
                    resistance_low_num = wholeRl + 1
                    resistance_moderate_num = wholeRm
                else:
                    resistance_low_num = wholeRl
                    resistance_moderate_num = wholeRm + 1


        elif fitness_level==FitnessLevel.INTERMEDIATE:

            endurance_moderate_num=0.75*endurance_num
            endurance_high_num=0.25*endurance_num
            fractionalEm, wholeEm = math.modf(endurance_moderate_num)
            fractionalEh, wholeEh = math.modf(endurance_high_num)
            if fractionalEm > 0.5:
                endurance_moderate_num = wholeEm + 1
                endurance_high_num = wholeEh
            elif fractionalEh > 0.5:
                endurance_moderate_num = wholeEm
                endurance_high_num = wholeEh + 1
            elif fractionalEm == 0.5:
                if endurance_moderate_num > endurance_high_num:
                    endurance_moderate_num = wholeEm + 1
                    endurance_high_num = wholeEh
                else:
                    endurance_moderate_num = wholeEm
                    endurance_high_num = wholeEh + 1
            resistance_moderate_num=0.75*resistance_num
            resistance_high_num=0.25*resistance_num
            fractionalRm, wholeRm = math.modf(resistance_moderate_num)
            fractionalRh, wholeRh = math.modf(resistance_high_num)
            if fractionalRm > 0.5:
                resistance_moderate_num = wholeRm + 1
                resistance_high_num = wholeRh
            elif fractionalRh > 0.5:
                resistance_moderate_num = wholeRm
                resistance_high_num = wholeRh + 1
            elif fractionalRm == 0.5:
                if resistance_moderate_num > resistance_high_num:
                    resistance_moderate_num = wholeRm + 1
                    resistance_high_num = wholeRh
                else:
                    resistance_moderate_num = wholeRm
                    resistance_high_num = wholeRh + 1



        elif fitness_level==FitnessLevel.FIT:
            endurance_moderate_num = 0.25 * endurance_num
            endurance_high_num = 0.75 * endurance_num
            resistance_moderate_num = 0.25 * resistance_num
            resistance_high_num = 0.75 * resistance_num
            fractionalEm, wholeEm = math.modf(endurance_moderate_num)
            fractionalEh, wholeEh = math.modf(endurance_high_num)
            if fractionalEm > 0.5:
                endurance_moderate_num = wholeEm + 1
                endurance_high_num = wholeEh
            elif fractionalEh > 0.5:
                endurance_moderate_num = wholeEm
                endurance_high_num = wholeEh + 1
            elif fractionalEm == 0.5:
                if endurance_moderate_num > endurance_high_num:
                    endurance_moderate_num = wholeEm + 1
                    endurance_high_num = wholeEh
                else:
                    endurance_moderate_num = wholeEm
                    endurance_high_num = wholeEh + 1

            fractionalRm, wholeRm = math.modf(resistance_moderate_num)
            fractionalRh, wholeRh = math.modf(resistance_high_num)
            if fractionalRm > 0.5:
                resistance_moderate_num = wholeRm + 1
                resistance_high_num = wholeRh
            elif fractionalRh > 0.5:
                resistance_moderate_num = wholeRm
                resistance_high_num = wholeRh + 1
            elif fractionalRm == 0.5:
                if resistance_moderate_num > resistance_high_num:
                    resistance_moderate_num = wholeRm + 1
                    resistance_high_num = wholeRh
                else:
                    resistance_moderate_num = wholeRm
                    resistance_high_num = wholeRh + 1

        elif fitness_level==FitnessLevel.VERYFIT:
            endurance_high_num=endurance_num
            resistance_high_num=resistance_num



        print('****',endurance_high_num)
        print('*****',endurance_moderate_num)

        print(resistance_high_num)
        print(resistance_moderate_num)

        print('**********')
        if fitness_level == FitnessLevel.NEVEREXERCISED:
            low_e_combination=list(itertools.combinations(low_intensities_endurance,int(endurance_low_num)))
            low_r_combination=list(itertools.combinations(low_intensities_resistance,int(resistance_low_num)))
            counter=1


            for low_e in low_e_combination:
                if(counter > num_weeks):
                    break
                for low_r in low_r_combination:
                    if (counter > num_weeks):
                        break
                    if counter <= num_weeks:
                        print(calculate_calorie_tuple(low_e,plan.weight))
                        print(calculate_calorie_tuple(low_r,plan.weight))
                        if calorie_burn_exercise - 50 < calculate_calorie_tuple(low_e,plan.weight) + calculate_calorie_tuple(low_r,plan.weight) < calorie_burn_exercise + 50:
                            workouts=list(low_e) + list(low_r)
                            print(workouts)
                            wplan=WorkoutPlan(week=counter, user_id=user.id,workouts=workouts)
                            counter = counter + 1
                            db.session.add(wplan)

            db.session.commit()

        elif(fitness_level== FitnessLevel.BEGINNER):
            print('end low****',endurance_low_num)
            print(endurance_moderate_num)
            print(resistance_low_num)
            print(resistance_moderate_num)
            print('*******')
            low_e_combination=list(itertools.combinations(low_intensities_endurance,int(endurance_low_num)))
            moderate_e_combination=list(itertools.combinations(moderate_intensities_endurance,int(endurance_moderate_num)))
            low_r_combination=list(itertools.combinations(low_intensities_resistance,int(resistance_low_num)))
            moderate_r_combination=list(itertools.combinations(moderate_intensities_resistance,int(resistance_moderate_num)))
            counter=1
            for low_e in low_e_combination:
                if (counter > num_weeks):
                    break
                for moderate_e in moderate_e_combination:
                    if(counter > num_weeks):
                        break
                    for low_r in low_r_combination:
                        if(counter > num_weeks):
                            break
                        for moderate_r in moderate_r_combination:
                            if(counter > num_weeks):
                                break
                            if counter<=num_weeks:
                                if calorie_burn_exercise - 50 < calculate_calorie_tuple(low_e,plan.weight) + calculate_calorie_tuple(moderate_e,plan.weight) + calculate_calorie_tuple(low_r,plan.weight) + calculate_calorie_tuple(moderate_r,plan.weight) < calorie_burn_exercise + 50:

                                    workouts = list(low_e) + list(moderate_e) + list(low_r) + list(moderate_r)
                                    wplan = WorkoutPlan(week=counter, user_id=user.id, workouts=workouts)
                                    print(workouts)
                                    counter = counter + 1
                                    db.session.add(wplan)

            db.session.commit()
        elif (fitness_level == FitnessLevel.INTERMEDIATE or fitness_level==FitnessLevel.FIT):
            high_e_combination = list(itertools.combinations(high_intensities_endurance, int(endurance_high_num)))

            moderate_e_combination = list(
                itertools.combinations(moderate_intensities_endurance, int(endurance_moderate_num)))
            high_r_combination = list(itertools.combinations(high_intensities_resistance, int(resistance_high_num)))
            moderate_r_combination = list(
                itertools.combinations(moderate_intensities_resistance, int(resistance_moderate_num)))
            counter = 1
            for mod_e in moderate_e_combination:
                if (counter > num_weeks):
                    break
                for high_e in high_e_combination:
                    if (counter > num_weeks):
                        break
                    for mod_r in moderate_r_combination:
                        if (counter > num_weeks):
                            break
                        for high_r in high_r_combination:
                            if (counter > num_weeks):
                                break

                            if counter <= num_weeks:
                                csum2=calculate_calorie_tuple(mod_e,plan.weight) + calculate_calorie_tuple(high_e,plan.weight) + calculate_calorie_tuple(
                                    mod_r,plan.weight) + calculate_calorie_tuple(high_r,plan.weight)
                               # print(csum2)
                                if calorie_burn_exercise - 50 < calculate_calorie_tuple(mod_e,plan.weight) + calculate_calorie_tuple(high_e,plan.weight) + calculate_calorie_tuple(
                                    mod_r,plan.weight) + calculate_calorie_tuple(high_r,plan.weight) < calorie_burn_exercise + 50:
                                    workouts = list(mod_e) + list(high_e) + list(mod_r) + list(high_r)
                                    wplan = WorkoutPlan(week=counter, user_id=user.id, workouts=workouts)
                                    print(workouts)
                                    counter = counter + 1
                                    db.session.add(wplan)

            db.session.commit()
        elif fitness_level == FitnessLevel.VERYFIT:
            high_e_combination=list(itertools.combinations(high_intensities_endurance,int(endurance_high_num)))
            high_r_combination=list(itertools.combinations(high_intensities_resistance,int(resistance_high_num)))
            counter=1


            for high_e in high_e_combination:
                if(counter > num_weeks):
                    break
                for high_r in high_r_combination:
                    if (counter > num_weeks):
                        break
                    if counter <= num_weeks:

                        if calorie_burn_exercise - 50 < calculate_calorie_tuple(high_e,plan.weight) + calculate_calorie_tuple(high_r,plan.weight) < calorie_burn_exercise + 50:
                            workouts=list(high_e) + list(high_r)
                            print(workouts)
                            for w in workouts:
                                print(w.intensity)
                            wplan=WorkoutPlan(week=counter, user_id=user.id,workouts=workouts)
                            counter = counter + 1
                            db.session.add(wplan)

            db.session.commit()













class Type:
    RESISTANCETRAINING=1
    ENDURANCETRAINING=2
    MOBILITYTRAINING=3


class Intensity:
    LOWINTENSITY=1
    MODERATEINTENSITY=2
    HIGHINTENSITY=3







class FitnessLevel:
    NEVEREXERCISED = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    FIT = 4
    VERYFIT = 5



