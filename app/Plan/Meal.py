
from .. import db




class MealPlan(db.Model):
    __tablename__='mealplans'

    id = db.Column(db.Integer, primary_key=True)
    breakfast_id=db.Column(db.Integer,db.ForeignKey('breakfasts.id'))
    lunch_id=db.Column(db.Integer,db.ForeignKey('lunches.id'))
    dinner_id=db.Column(db.Integer,db.ForeignKey('Dinners.id'))
    snack_id=db.Column(db.Integer,db.ForeignKey('snackes.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))





    def valid_meal_plan(self):
        flag=True
        meals= db.session.query(MealPlan).filter_by(user_id=self.user.id).all()
        for i in range(len(meals)):
            if (self.breakfast_id == meals[i].breakfast_id and self.lunch_id == meals[i].lunch_id and self.dinner_id ==meals[i].dinner_id) or \
                    (self.lunch_id == meals[i].lunch_id and self.dinner_id == meals[i].dinner_id and self.snack_id == meals[i].snack_id) or \
                    (self.breakfast_id == meals[i].breakfast_id and self.dinner_id == meals[i].dinner_id and self.snack_id == meals[i].snack_id) or \
                    (self.breakfast_id == meals[i].breakfast_id and self.lunch_id == meals[i].lunch_id and self.snack_id == meals[i].snack_id):
                flag=False
                break
        print(flag)
        return flag


    @staticmethod
    def create_meal_plan(user,daily_calorie_intake,plan):
        MealPlan.query.filter_by(user_id=user.id).delete()

        db.session.commit()
        meal_category=plan.meal_category
        breakfasts=Breakfast.query.all()
        lunches=Lunch.query.all()
        dinners=Dinner.query.all()
        snackes=Snack.query.all()
        recommended_calorie=daily_calorie_intake

        pair_map = {}
        unique=0;
        for i in range(len(breakfasts)):
            for j in range(len(lunches)):
                calorie_sum=breakfasts[i].calories + lunches[j].calories
                pair_map[unique]= []
                pair_map[unique].append(breakfasts[i])
                pair_map[unique].append(lunches[j])
                unique=unique+1

        for i in range(len(dinners)):
            for j in range(len(snackes)):
                current_sum=dinners[i].calories + snackes[j].calories
                for key, value in pair_map.items():
                    checked_calorie=value[0].calories + value[1].calories+current_sum
                    if recommended_calorie-50 < checked_calorie < recommended_calorie + 50 :
                        mealplan=MealPlan(breakfast=value[0],lunch=value[1],dinner=dinners[i],snack=snackes[j],user=user)
                        db.session.expunge(mealplan)
                        if mealplan.valid_meal_plan():
                            if meal_category==2:
                                if(value[0].category==value[1].category==snackes[j].category==dinners[i].category==2):
                                    db.session.add(mealplan)
                            else:


                                db.session.add(mealplan)
                                print(mealplan)

        db.session.commit()





class Breakfast(db.Model):
    __tablename__='breakfasts'
    __searchable__=['name','ingredients']
    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text)
    description=db.Column(db.Text)
    calories=db.Column(db.FLOAT)
    category = db.Column(db.Integer, default=1)
    ingredients=db.Column(db.Text,default='')
    carb = db.Column(db.Float, default=0)
    protein = db.Column(db.Float, default=0)
    fat = db.Column(db.Float, default=0)
    duration=db.Column(db.Text,default='')

    meal_plans=db.relationship('MealPlan',backref='breakfast',lazy='dynamic')
    image_url=db.Column(db.Text,default='https://thumbs.dreamstime.com/b/balanced-diet-food-background-balanced-diet-food-background-organic-food-healthy-nutrition-superfoods-meat-fish-legumes-nuts-121936796.jpg')
    def to_json(self):
        json_breakfast={
            'id': self.id,
            'name': self.name,
            'description':self.description,
            'calories':self.calories,
            'category': self.category,
            'ingredients':self.ingredients,
            'carb':self.carb,
            'protein':self.protein,
            'fat':self.fat,
            'duration': self.duration,
            'image_url': self.image_url

        }
        return json_breakfast



class Lunch(db.Model):
    __tablename__='lunches'
    __searchable__ = ['name', 'ingredients']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    calories = db.Column(db.FLOAT)
    category = db.Column(db.Integer, default=1)
    ingredients = db.Column(db.Text, default='')
    carb = db.Column(db.Float, default=0)
    protein = db.Column(db.Float, default=0)
    fat = db.Column(db.Float, default=0)
    duration = db.Column(db.Text, default='')
    meal_plans=db.relationship('MealPlan',backref='lunch',lazy='dynamic')
    image_url = db.Column(db.Text,
                          default='https://thumbs.dreamstime.com/b/balanced-diet-food-background-balanced-diet-food-background-organic-food-healthy-nutrition-superfoods-meat-fish-legumes-nuts-121936796.jpg')


    def to_json(self):
        json_lunch = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'calories': self.calories,
            'category': self.category,
            'ingredients': self.ingredients,
            'carb': self.carb,
            'protein': self.protein,
            'fat': self.fat,
            'duration': self.duration,
            'image_url': self.image_url

        }
        return json_lunch





class Dinner(db.Model):
    __tablename__='Dinners'
    __searchable__ = ['name', 'ingredients']
    id =db.Column(db.Integer, primary_key=True)
    name=db.Column(db.Text)
    description =db.Column(db.Text)
    calories =db.Column(db.FLOAT)
    category = db.Column(db.Integer, default=1)
    ingredients = db.Column(db.Text, default='')
    carb = db.Column(db.Float, default=0)
    protein = db.Column(db.Float, default=0)
    fat = db.Column(db.Float, default=0)
    duration = db.Column(db.Text, default='')
    meal_plans=db.relationship('MealPlan',backref='dinner',lazy='dynamic')
    image_url = db.Column(db.Text,
                          default='https://thumbs.dreamstime.com/b/balanced-diet-food-background-balanced-diet-food-background-organic-food-healthy-nutrition-superfoods-meat-fish-legumes-nuts-121936796.jpg')

    def to_json(self):
        json_dinner = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'calories': self.calories,
            'category': self.category,
            'ingredients': self.ingredients,
            'carb': self.carb,
            'protein': self.protein,
            'fat': self.fat,
            'duration': self.duration,
            'image_url': self.image_url


        }
        return json_dinner



class Snack(db.Model):
    __tablename__='snackes'
    __searchable__ = ['name', 'ingredients']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    description = db.Column(db.Text)
    calories = db.Column(db.FLOAT)
    category =db.Column(db.Integer,default=1)
    ingredients = db.Column(db.Text, default='')
    carb = db.Column(db.Float, default=0)
    protein = db.Column(db.Float, default=0)
    fat = db.Column(db.Float, default=0)
    duration = db.Column(db.Text, default='')
    meal_plans=db.relationship('MealPlan',backref='snack',lazy='dynamic')
    image_url = db.Column(db.Text,
                          default='https://thumbs.dreamstime.com/b/balanced-diet-food-background-balanced-diet-food-background-organic-food-healthy-nutrition-superfoods-meat-fish-legumes-nuts-121936796.jpg')

    def to_json(self):
        json_snack = {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'calories': self.calories,
            'category': self.category,
            'ingredients': self.ingredients,
            'carb': self.carb,
            'protein': self.protein,
            'fat': self.fat,
            'duration': self.duration,
            'image_url': self.image_url

        }
        return json_snack

class FoodLog(db.Model):
    __tablename__='foodlogs'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    calories = db.Column(db.FLOAT)
    category=db.Column(db.Integer)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    def to_json(self):
        json_log = {
            'name': self.name,
            'calories': self.calories,
            'category': self.category,

        }
        return json_log



class Category:
    VEGETERIAN=2
    TRADITIONAL=1




class TypeMeal:
    all=0
    breakfast=1
    lunch=2
    dinner=4
    snack=8

    def __init__(self,type2):
        self.type2=type2

    def has_meal(self, meal):
        return self.type2 & meal == meal


