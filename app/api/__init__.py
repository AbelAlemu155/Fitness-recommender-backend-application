from flask import Blueprint
api=Blueprint('api',__name__)

from . import authentication,decorators,errors,posts,users,plan,useractivity,search,workout,search_workout,upload,trainer,food
