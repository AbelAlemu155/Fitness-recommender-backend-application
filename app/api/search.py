from flask import jsonify, request, url_for, g, current_app

from app import db
from app.Plan.Meal import TypeMeal, Breakfast, Lunch, Dinner, Snack
from app.api import api


@api.route('/searchfood',methods=['POST'])
def search_food():
    per_page=15
    page=request.get_json(force=True).get('page')
    keyword=request.get_json(force=True).get('keyword')
    type=request.get_json(force=True).get('type')
    count=request.get_json(force=True).get('count')
    category=request.get_json(force=True).get('category')
    #category is 1 or 2
    sort=request.get_json().get('calorie')
    #calorie is True or False

    per_page = 15
    b_query = Breakfast.query.msearch(keyword)
    l_query = Lunch.query.msearch(keyword)
    d_query = Dinner.query.msearch(keyword)
    s_query = Snack.query.msearch(keyword)
    bfs = []
    ls = []
    ds = []
    ss = []
    foods = []
    tymeal = TypeMeal(type2=type)
    if type == 0:
        if category == 2:
            b_query = b_query.filter_by(category=category)
            l_query = l_query.filter_by(category=category)
            d_query = d_query.filter_by(category=category)
            s_query = s_query.filter_by(category=category)

        b_page = b_query.paginate(page, per_page=4, error_out=False)
        l_page = l_query.paginate(page, per_page=4, error_out=False)
        d_page = d_query.paginate(page, per_page=4, error_out=False)
        s_page = s_query.paginate(page, per_page=3, error_out=False)
        prev = None
        if b_page.has_prev or l_page.has_prev or d_page.has_prev or s_page.has_prev:
            prev = url_for('api.search_food', page=page - 1)
        next = None
        if b_page.has_next or l_page.has_next or s_page.has_next or d_page.has_next:
            next = url_for('api.search_food', page=page + 1)
        foods = b_page.items + l_page.items + d_page.items + s_page.items
        if not sort:
            return jsonify({
                'meal': [m.to_json() for m in foods],
                'prev_url': prev,
                'next_url': next,
                'count_b': b_page.total,
                'count_l': l_page.total,
                'count_d': d_page.total,
                'count_s': s_page.total
            })
        else:
            foods.sort(key=lambda x: x.calories)
            return jsonify({
                'meal': [m.to_json() for m in foods],
                'prev_url': prev,
                'next_url': next,
                'count_b': b_page.total,
                'count_l': l_page.total,
                'count_d': d_page.total,
                'count_s': s_page.total
            })

    else:
        if category == 2:
            b_query = b_query.filter_by(category=category)
            l_query = l_query.filter_by(category=category)
            d_query = d_query.filter_by(category=category)
            s_query = s_query.filter_by(category=category)

        if count == 1:
            b_page = b_query.paginate(page, per_page=15, error_out=False)
            l_page = l_query.paginate(page, per_page=15, error_out=False)
            d_page = d_query.paginate(page, per_page=15, error_out=False)
            s_page = s_query.paginate(page, per_page=15, error_out=False)
            prev = None

            if tymeal.has_meal(1):
                foods = b_page.items
                if b_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
                if not sort:
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': b_page.total,
                        'count_l': 0,
                        'count_d': 0,
                        'count_s': 0
                    })
                else:
                    foods.sort(key=lambda x: x.calories)
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': b_page.total,
                        'count_l': 0,
                        'count_d': 0,
                        'count_s': 0
                    })

            elif tymeal.has_meal(2):
                if l_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
                foods = l_page.items
                if not sort:
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': l_page.total,
                        'count_d': 0,
                        'count_s': 0
                    })
                else:
                    foods.sort(key=lambda x: x.calories)
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': l_page.total,
                        'count_d': 0,
                        'count_s': 0
                    })
            elif (tymeal.has_meal(4)):
                if d_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if d_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
                foods = d_page.items
                if not sort:
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': 0,
                        'count_d': d_page.total,
                        'count_s': 0
                    })
                else:
                    foods.sort(key=lambda x: x.calories)
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': 0,
                        'count_d': d_page.total,
                        'count_s': 0
                    })


            elif (tymeal.has_meal(8)):
                if s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
                foods = s_page.items
                if not sort:
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': 0,
                        'count_d': 0,
                        'count_s': s_page.total
                    })
                else:
                    foods.sort(key=lambda x: x.calories)
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': 0,
                        'count_d': 0,
                        'count_s': s_page.total
                    })

        elif count == 2:
            b_page = b_query.paginate(page, per_page=8, error_out=False)
            l_page = l_query.paginate(page, per_page=8, error_out=False)
            d_page = d_query.paginate(page, per_page=8, error_out=False)
            s_page = s_query.paginate(page, per_page=8, error_out=False)
            foods = []
            b = False
            bc = 0
            lc = 0
            dc = 0
            sc = 0
            l = False
            d = False
            s = False
            prev = None
            if tymeal.has_meal(1):
                b = True
                bc = b_page.total
                foods = foods + b_page.items
            if tymeal.has_meal(2):
                l = True
                lc = l_page.total
                foods = foods + l_page.items
            if (tymeal.has_meal(4)):
                d = True
                dc = d_page.total
                foods = foods + d_page.items
            if (tymeal.has_meal(8)):
                sc = s_page.total
                s = True
                foods = foods + s_page.items
            if b and l:
                if b_page.has_prev or l_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or l_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
            elif b and d:
                if b_page.has_prev or d_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or d_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif b and s:
                if b_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
            elif l and d:
                if l_page.has_prev or d_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next or d_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif l and s:
                if l_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
            elif d and s:
                if s_page.has_prev or d_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
            next = None
            if s_page.has_next or d_page.has_next:
                next = url_for('api.search_food', page=page + 1)
            if not sort:
                return jsonify({
                    'meal': [m.to_json() for m in foods],
                    'prev_url': prev,
                    'next_url': next,
                    'count_b': bc,
                    'count_l': lc,
                    'count_d': dc,
                    'count_s': sc
                })


            else:
                foods.sort(key=lambda x: x.calories)
                return jsonify({
                    'meal': [m.to_json() for m in foods],
                    'prev_url': prev,
                    'next_url': next,
                    'count_b': bc,
                    'count_l': lc,
                    'count_d': dc,
                    'count_s': sc
                })

        elif count == 3:
            b_page = b_query.paginate(page, per_page=5, error_out=False)
            l_page = l_query.paginate(page, per_page=5, error_out=False)
            d_page = d_query.paginate(page, per_page=5, error_out=False)
            s_page = s_query.paginate(page, per_page=5, error_out=False)

            foods = []
            b = False
            bc = 0
            lc = 0
            dc = 0
            sc = 0
            l = False
            d = False
            s = False
            prev = None
            if tymeal.has_meal(1):
                b = True
                bc = b_page.total
                foods = foods + b_page.items
            if tymeal.has_meal(2):
                l = True
                lc = l_page.total
                foods = foods + l_page.items
            if (tymeal.has_meal(4)):
                d = True
                dc = d_page.total
                foods = foods + d_page.items
            if (tymeal.has_meal(8)):
                sc = s_page.total
                s = True
                foods = foods + s_page.items

            if (b and l and d):
                if b_page.has_prev or d_page.has_prev or l_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or d_page.has_next or l_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif (b and d and s):
                if b_page.has_prev or d_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or d_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif (l and d and s):
                if l_page.has_prev or d_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next or d_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif (b and l and s):
                if l_page.has_prev or b_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next or b_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            if not sort:
                return jsonify({
                    'meal': [m.to_json() for m in foods],
                    'prev_url': prev,
                    'next_url': next,
                    'count_b': bc,
                    'count_l': lc,
                    'count_d': dc,
                    'count_s': sc
                })


            else:
                foods.sort(key=lambda x: x.calories)
                return jsonify({
                    'meal': [m.to_json() for m in foods],
                    'prev_url': prev,
                    'next_url': next,
                    'count_b': bc,
                    'count_l': lc,
                    'count_d': dc,
                    'count_s': sc
                })







def query_foods(page,keyword,type,count,category,sort):
    per_page=15
    b_query = Breakfast.query.msearch(keyword)
    l_query = Lunch.query.msearch(keyword)
    d_query = Dinner.query.msearch(keyword)
    s_query = Snack.query.msearch(keyword)
    bfs = []
    ls = []
    ds = []
    ss = []
    foods = []
    tymeal = TypeMeal(type2=type)
    if type == 0:
        if category == 2:
            b_query = b_query.filter_by(category=category)
            l_query = l_query.filter_by(category=category)
            d_query = d_query.filter_by(category=category)
            s_query = s_query.filter_by(category=category)

        b_page = b_query.paginate(page, per_page=4, error_out=False)
        l_page = l_query.paginate(page, per_page=4, error_out=False)
        d_page = d_query.paginate(page, per_page=4, error_out=False)
        s_page = s_query.paginate(page, per_page=3, error_out=False)
        prev = None
        if b_page.has_prev or l_page.has_prev or d_page.has_prev or s_page.has_prev:
            prev = url_for('api.search_food', page=page - 1)
        next = None
        if b_page.has_next or l_page.has_next or s_page.has_next or d_page.has_next:
            next = url_for('api.search_food', page=page + 1)
        foods = b_page.items + l_page.items + d_page.items + s_page.items
        if not sort:
            return jsonify({
                'meal': [m.to_json() for m in foods],
                'prev_url': prev,
                'next_url': next,
                'count_b': b_page.total,
                'count_l': l_page.total,
                'count_d': d_page.total,
                'count_s': s_page.total
            })
        else:
            foods.sort(key=lambda x: x.calories)
            return jsonify({
                'meal': [m.to_json() for m in foods],
                'prev_url': prev,
                'next_url': next,
                'count_b': b_page.total,
                'count_l': l_page.total,
                'count_d': d_page.total,
                'count_s': s_page.total
            })

    else:
        if category == 2:
            b_query = b_query.filter_by(category=category)
            l_query = l_query.filter_by(category=category)
            d_query = d_query.filter_by(category=category)
            s_query = s_query.filter_by(category=category)

        if count == 1:
            b_page = b_query.paginate(page, per_page=15, error_out=False)
            l_page = l_query.paginate(page, per_page=15, error_out=False)
            d_page = d_query.paginate(page, per_page=15, error_out=False)
            s_page = s_query.paginate(page, per_page=15, error_out=False)
            prev = None

            if tymeal.has_meal(1):
                foods = b_page.items
                if b_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
                if not sort:
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': b_page.total,
                        'count_l': 0,
                        'count_d': 0,
                        'count_s': 0
                    })
                else:
                    foods.sort(key=lambda x: x.calories)
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': b_page.total,
                        'count_l': 0,
                        'count_d': 0,
                        'count_s': 0
                    })

            elif tymeal.has_meal(2):
                if l_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
                foods = l_page.items
                if not sort:
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': l_page.total,
                        'count_d': 0,
                        'count_s': 0
                    })
                else:
                    foods.sort(key=lambda x: x.calories)
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': l_page.total,
                        'count_d': 0,
                        'count_s': 0
                    })
            elif (tymeal.has_meal(4)):
                if d_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if d_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
                foods = d_page.items
                if not sort:
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': 0,
                        'count_d': d_page.total,
                        'count_s': 0
                    })
                else:
                    foods.sort(key=lambda x: x.calories)
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': 0,
                        'count_d': d_page.total,
                        'count_s': 0
                    })


            elif (tymeal.has_meal(8)):
                if s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
                foods = s_page.items
                if not sort:
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': 0,
                        'count_d': 0,
                        'count_s': s_page.total
                    })
                else:
                    foods.sort(key=lambda x: x.calories)
                    return jsonify({
                        'meal': [m.to_json() for m in foods],
                        'prev_url': prev,
                        'next_url': next,
                        'count_b': 0,
                        'count_l': 0,
                        'count_d': 0,
                        'count_s': s_page.total
                    })

        elif count == 2:
            b_page = b_query.paginate(page, per_page=8, error_out=False)
            l_page = l_query.paginate(page, per_page=8, error_out=False)
            d_page = d_query.paginate(page, per_page=8, error_out=False)
            s_page = s_query.paginate(page, per_page=8, error_out=False)
            foods = []
            b = False
            bc = 0
            lc = 0
            dc = 0
            sc = 0
            l = False
            d = False
            s = False
            prev = None
            if tymeal.has_meal(1):
                b = True
                bc = b_page.total
                foods = foods + b_page.items
            if tymeal.has_meal(2):
                l = True
                lc = l_page.total
                foods = foods + l_page.items
            if (tymeal.has_meal(4)):
                d = True
                dc = d_page.total
                foods = foods + d_page.items
            if (tymeal.has_meal(8)):
                sc = s_page.total
                s = True
                foods = foods + s_page.items
            if b and l:
                if b_page.has_prev or l_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or l_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
            elif b and d:
                if b_page.has_prev or d_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or d_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif b and s:
                if b_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
            elif l and d:
                if l_page.has_prev or d_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next or d_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif l and s:
                if l_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
            elif d and s:
                if s_page.has_prev or d_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if s_page.has_next or d_page.has_next:
                    next = url_for('api.search_food', page=page + 1)
            if not sort:
                return jsonify({
                    'meal': [m.to_json() for m in foods],
                    'prev_url': prev,
                    'next_url': next,
                    'count_b': bc,
                    'count_l': lc,
                    'count_d': dc,
                    'count_s': sc
                })


            else:
                foods.sort(key=lambda x: x.calories)
                return jsonify({
                    'meal': [m.to_json() for m in foods],
                    'prev_url': prev,
                    'next_url': next,
                    'count_b': bc,
                    'count_l': lc,
                    'count_d': dc,
                    'count_s': sc
                })

        elif count == 3:
            b_page = b_query.paginate(page, per_page=5, error_out=False)
            l_page = l_query.paginate(page, per_page=5, error_out=False)
            d_page = d_query.paginate(page, per_page=5, error_out=False)
            s_page = s_query.paginate(page, per_page=5, error_out=False)

            foods = []
            b = False
            bc = 0
            lc = 0
            dc = 0
            sc = 0
            l = False
            d = False
            s = False
            prev = None
            if tymeal.has_meal(1):
                b = True
                bc = b_page.total
                foods = foods + b_page.items
            if tymeal.has_meal(2):
                l = True
                lc = l_page.total
                foods = foods + l_page.items
            if (tymeal.has_meal(4)):
                d = True
                dc = d_page.total
                foods = foods + d_page.items
            if (tymeal.has_meal(8)):
                sc = s_page.total
                s = True
                foods = foods + s_page.items

            if (b and l and d):
                if b_page.has_prev or d_page.has_prev or l_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or d_page.has_next or l_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif (b and d and s):
                if b_page.has_prev or d_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if b_page.has_next or d_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif (l and d and s):
                if l_page.has_prev or d_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next or d_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            elif (b and l and s):
                if l_page.has_prev or b_page.has_prev or s_page.has_prev:
                    prev = url_for('api.search_food', page=page - 1)
                next = None
                if l_page.has_next or b_page.has_next or s_page.has_next:
                    next = url_for('api.search_food', page=page + 1)

            if not sort:
                return jsonify({
                    'meal': [m.to_json() for m in foods],
                    'prev_url': prev,
                    'next_url': next,
                    'count_b': bc,
                    'count_l': lc,
                    'count_d': dc,
                    'count_s': sc
                })


            else:
                foods.sort(key=lambda x: x.calories)
                return jsonify({
                    'meal': [m.to_json() for m in foods],
                    'prev_url': prev,
                    'next_url': next,
                    'count_b': bc,
                    'count_l': lc,
                    'count_d': dc,
                    'count_s': sc
                })


















