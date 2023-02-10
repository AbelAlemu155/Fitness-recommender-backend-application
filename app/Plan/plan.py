from app import db
from app.Plan import MealPlan


class UserPlan(db.Model):
    __tablename__ = 'plans'
    id = db.Column(db.Integer, primary_key=True)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    height = db.Column(db.FLOAT, nullable=False)
    weight = db.Column(db.FLOAT, nullable=False)
    goal = db.Column(db.Integer, nullable=False)
    goal_weight = db.Column(db.FLOAT, nullable=False)
    le_activity = db.Column(db.Integer, nullable=False)
    fitness_level = db.Column(db.Integer, nullable=False)
    meal_category = db.Column(db.Integer)
    physical_limitation = db.Column(db.String(20), nullable=False)
    num_of_days_workout = db.Column(db.Integer, nullable=False)
    requires_motivation = db.Column(db.BOOLEAN, default=False)
    num_of_days_goal = db.Column(db.Integer)
    num_of_weeks_goal = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    @staticmethod
    def from_json(json_plan,user):
        user_id=user.id
        age=json_plan.get('age')
        gender=json_plan.get('gender')
        height=json_plan.get('height')
        weight=json_plan.get('weight')
        goal=json_plan.get('goal')
        goal_weight=json_plan.get('goal_weight')
        le_activity=json_plan.get('le_activity')
        fitness_level=json_plan.get('fitness_level')
        meal_category=json_plan.get('meal_category')
        physical_limitation='none'
        num_of_days_workout=json_plan.get('num_of_days_workout')
        num_of_weeks_goal=json_plan.get('num_of_weeks_goal')
        return UserPlan(user_id=user_id,age=age,gender=gender,height=height,weight=weight,goal=goal,goal_weight=goal_weight,le_activity=le_activity,fitness_level=fitness_level,
                        meal_category=meal_category,physical_limitation=physical_limitation,num_of_days_workout=num_of_days_workout,num_of_weeks_goal=num_of_weeks_goal)



    def to_json(self):
        json_up={
            'height': self.height,
            'weight': self.weight,
            'goal': self.goal,
            'goal_weight': self.goal_weight,
            'le_activity': self.le_activity,
            'fitness_level' : self.fitness_level,
        }
        return json_up






    # a constructor to handle automatic assigning of attributes
    def __init__(self,**kwargs):
        super(UserPlan,self).__init__(**kwargs)
        self.num_of_days_goal=7*self.num_of_weeks_goal




    # a method that is called to create all plans of a particular user
    def create_user_plan(self, user):
        rec_intake = self.daily_calorie_intake()
        user.daily_calorie_intake = rec_intake
        user.plan_id=self.id
        db.session.add(user)
        db.session.commit()
        # creating meal plan for the user
        MealPlan.create_meal_plan(user, rec_intake,self)
       # WorkoutPlan.create_workout_plan(user,self)



    #a method that is used to calculate the resting metabolic rate by using mifflin st jeor equation
    #weight in Kg and height in centimeters
    def calculate_rmr(self):
        if (self.gender == 'F'):
            rmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161
            return rmr
        rmr = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        return rmr



    #Per day calorie need based on rmr and activity
    def calculate_total_calorie_needs(self):
        rmr = self.calculate_rmr()
        if (self.le_activity == ActivityLevel.SEDENTARY):
            return 1.2 * rmr
        elif (self.le_activity == ActivityLevel.JUSTWALKING):
            return 1.375 * rmr
        elif (self.le_activity == ActivityLevel.MODERATEXERCISE):
            return 1.55 * rmr
        elif (self.le_activity == ActivityLevel.INTENSEEXERCISE):
            return 1.725 * rmr



    #the total calorie surplus or deficit to meet goal, for maintaining weight=0
    def calorie_to_meet_goal(self):
        diff = self.goal_weight - self.weight
        if diff < 0:
            calorie_diff = 3500 * diff / 0.45359

        else:
            calorie_diff = 7000 * diff

        return calorie_diff




    #for the plan how much of a calorie loss is recommended by exercise
    def calorie_loss_by_exercise(self):
        diff = self.goal_weight - self.weight
        if diff < 0:
            return -1 * 0.2 * self.calorie_to_meet_goal()
        elif (diff > 0):
            return 0.3 * self.calorie_to_meet_goal()
        else:
            return 0.1*7 * self.calculate_total_calorie_needs()

    def recommended_water_intake(self):
        return 0.033* self.weight


   #meal daily plan
    def daily_calorie_intake(self):
        total_need = self.calculate_total_calorie_needs()

        print(self.le_activity)
        total_intake = total_need * 7 * self.num_of_weeks_goal + self.calorie_to_meet_goal() + self.calorie_loss_by_exercise()*self.num_of_weeks_goal

        daily_intake = total_intake / (self.num_of_weeks_goal * 7)
        if(daily_intake < 500):
            #unrealistic goal
            return 500

        return daily_intake


class ActivityLevel:
    SEDENTARY = 1
    JUSTWALKING = 2
    MODERATEXERCISE = 3
    INTENSEEXERCISE = 4


class Goal:
    WEIGHTLOSS = 1
    MAINTAININGWEIGHT = 2
    MUSCLEGAIN = 3


class FitnessLevel:
    NEVEREXERCISED = 1
    BEGINNER = 2
    INTERMEDIATE = 3
    FIT = 4
    VERYFIT = 5





