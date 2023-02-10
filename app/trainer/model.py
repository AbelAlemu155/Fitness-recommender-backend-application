from app import db


class Trainer(db.Model):

    id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    costPerHour = db.Column(db.Float)
    gender = db.Column(db.String(20))
    yearOfExperience = db.Column(db.Integer)
    approve = db.Column(db.Boolean, default=False)
    user = db.relationship('User', backref=db.backref('trainer'))
    
    def to_json(self):
        trainer = {
            "id" : self.id,
            "cost_per_hour": self.costPerHour,
            "gender": self.gender,
            "exp": self.yearOfExperience,
            "username" : self.user.username
        }
        return trainer

    @staticmethod
    def from_json(jsonData):
        costPerHour = jsonData.get('cost_per_hour')
        gender = jsonData.get('gender')
        yearOfExperience = jsonData.get('exp')
        return Trainer(costPerHour=costPerHour, gender=gender, yearOfExperience=yearOfExperience)


class TrainerClient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainer.id"))

    def to_json(self):
        client = {
            "client_id": self.client_id,
            "trainer_id": self.trainer_id
        }
        return client


class TrainerRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainer.id"))


class AssignFitnessPlan(db.Model):
    __tablename__ = "assign_fitness"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainer.id"))
    name = db.Column(db.String)
    weeks = db.Column(db.Integer)  # how many weeks to do fitness plan
    workouts = db.relationship("AssignWorkouts", backref="assign_fitness")

    def to_json(self):
        fitness_plan = {
            "fplan_id": self.id,
            "name": self.name,
            "client_id": self.client_id,
            "trainer_id": self.trainer_id,
            "weeks": self.weeks,
            "workouts": [workout.to_json() for workout in self.workouts],
        }
        return fitness_plan

    @staticmethod
    def from_json(jsonData):
        client_id = jsonData.get('client_id')
        trainer_id = jsonData.get('trainer_id')
        name = jsonData.get('name')
        weeks = jsonData.get('weeks')
        return AssignFitnessPlan(
            client_id=client_id,
            trainer_id=trainer_id,
            name=name,
            weeks=weeks,
        )


class AssignWorkouts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fplan_id = db.Column(db.Integer, db.ForeignKey("assign_fitness.id"))
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"))
    dayOfWeek = db.Column(db.Integer)  # which day of the week to do workout

    def to_json(self):
        workouts = {
            "fplan_id": self.fplan_id,
            "workout_id": self.workout_id,
            "dayOfWeek": self.dayOfWeek,
        }
        return workouts
    @staticmethod
    def from_json(jsonData):
        workout_id = jsonData.get('workout_id')
        dayOfWeek = jsonData.get('dayOfWeek')
        return AssignWorkouts(
            workout_id=workout_id,
            dayOfWeek=dayOfWeek
        )


class AssignDietPlan(db.Model):
    __tablename__ = "assign_diet"
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    trainer_id = db.Column(db.Integer, db.ForeignKey("trainer.id"))
    name = db.Column(db.String)
    weeks = db.Column(db.Integer)  # how many weeks to do diet plan
    meals = db.relationship("AssignFood", backref="assign_diet")

    def to_json(self):
        diet_plan = {
            "dplan_id": self.id,
            "name": self.name,
            "client_id": self.client_id,
            "trainer_id": self.trainer_id,
            "weeks": self.weeks,
            "meals": [meal.to_json() for meal in self.meals],
        }
        return diet_plan
    @staticmethod
    def from_json(jsonData):
        client_id = jsonData.get('client_id')
        trainer_id = jsonData.get('trainer_id')
        name = jsonData.get('name')
        weeks = jsonData.get('weeks')
        return AssignDietPlan(
            client_id=client_id,
            trainer_id=trainer_id,
            name=name,
            weeks=weeks,
        )


class AssignFood(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dplan_id = db.Column(db.Integer, db.ForeignKey("assign_diet.id"))
    breakfast_id = db.Column(db.Integer, db.ForeignKey("breakfasts.id"))
    lunch_id = db.Column(db.Integer, db.ForeignKey("lunches.id"))
    dinner_id = db.Column(db.Integer, db.ForeignKey("Dinners.id"))
    snack_id = db.Column(db.Integer, db.ForeignKey("snackes.id"))
    dayOfWeek = db.Column(db.Integer)  # which day of the week to eat

    def to_json(self):
        meals = {
            "dplan_id": self.dplan_id,
            "breakfast_id": self.breakfast_id,
            "lunch_id": self.lunch_id,
            "dinner_id": self.dinner_id,
            "snack_id": self.snack_id,
            "dayOfWeek": self.dayOfWeek
        }
        return meals
    @staticmethod
    def from_json(jsonData):
        breakfast_id = jsonData.get('breakfast_id')
        lunch_id = jsonData.get('lunch_id')
        dinner_id = jsonData.get('dinner_id')
        snack_id = jsonData.get('snack_id')
        dayOfWeek = jsonData.get('dayOfWeek')
        return AssignFood(
            breakfast_id=breakfast_id,
            lunch_id=lunch_id,
            dinner_id=dinner_id,
            snack_id=snack_id,
            dayOfWeek=dayOfWeek
        )