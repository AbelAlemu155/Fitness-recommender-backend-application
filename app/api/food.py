from flask import jsonify, request

from app import db
from app.Plan import Breakfast, Lunch, Dinner
from app.api import api

@api.route('/getbfast/<int:id>')
def getbfast(id):
    bf=Breakfast.query.get_or_404(id)
    return jsonify(bf.to_json())

@api.route('/getlunch/<int:id>')
def getlunch(id):
    l=Lunch.query.get_or_404(id)
    return jsonify(l.to_json())

@api.route('getdinner/<int:id>')
def getdinner(id):
    d = Dinner.query.get_or_404(id)
    return jsonify(d.to_json())

@api.route('/getbfastfromlist/',methods=['POST'])
def get_b_list():
    ids = request.get_json().get('ids')
    bfs=[]
    for i in ids:
        b=Breakfast.query.get_or_404(i)
        bfs.append(b)
    return jsonify([b2.to_json() for b2 in bfs])

@api.route('/getlunchfromlist/',methods=['POST'])
def get_l_list():
    ids = request.get_json().get('ids')
    ls=[]
    for i in ids:
        l=Lunch.query.get_or_404(i)
        ls.append(l)
    return jsonify([l2.to_json() for l2 in ls])

@api.route('/getdinnerfromlist/',methods=['POST'])
def get_d_list():
    ids = request.get_json().get('ids')
    ds=[]
    for i in ids:
        d=Dinner.query.get_or_404(i)
        ds.append(d)
    return jsonify([d2.to_json() for d2 in ds])










