from flask import request, jsonify, Blueprint
import requests
from flask_jwt_extended import jwt_required, get_jwt_identity

from models import Calories, User, db


entries_route = Blueprint('entries',__name__)

@entries_route.route('/entries', methods=['GET'])
def get_entries():
    user_id = User.query.filter_by(username=get_jwt_identity()).first.id
    date = request.args.get('date')

    entries_query = Calories.query.filter_by(user_id=user_id)
    if date:
        entries_query = entries_query.filter_by(date=date)

    entries = entries_query.all()
    result = []
    for entry in entries:
        result.append({
            'id': entry.id,
            'date': entry.date,
            'time': entry.time,
            'item': entry.item,
            'calories': entry.calories,
            'is_below_target': entry.is_below_target
        })

    return jsonify(result),200

@entries_route.route('entries', method=['POST'])
@jwt_required()
def create_entry():
    data = request.get_json()
    user_id = User.query.filter_by(username = get_jwt_identity()).first().id
    date = data['date']
    time = data['time']
    item = data['item']
    calories = data.get('calories')

    if not calories:
        calories = requests.get_calories_from_nutritionix(item)

    entry = Calories(
        user_id=user_id,
        date=date,
        time=time,
        item=item,
        calories=calories
    )


    #calories check
    total_calories = get_total_calories_for_day(user_id, date)
    target_calories = get_user_target_calories(user_id)
    if total_calories < target_calories:
        entry.is_below_target = True
    
    db.session.add(entry)
    db.session.commit()

    return jsonify({
        'message': 'Entry successfull',
        'data': entry
    }), 201







    