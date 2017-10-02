from datetime import datetime

from bcrypt import gensalt
from flask import request, abort
from itsdangerous import URLSafeSerializer

from glycemiq_server.api import api
from glycemiq_server.log_manager import logManager
from glycemiq_server.config import config_as_dict
from glycemiq_server.models import db, BgReading, InsulinDose, Food, User

logger = logManager.get_logger(__name__)
config = config_as_dict('API')


@api.route('/handshake', methods=['GET'])
def handshake(email):
    """
    Client requests token from server.
    Token is sent to authorize all subsequent requests.
    """
    serializer = URLSafeSerializer(config['TOKEN_SECRET_KEY'])
    salt = gensalt().decode("utf-8")
    client_token = serializer.dumps(email, salt=salt)

    return salt + client_token


@api.route('/food', methods=['POST'])
def save_food(token, user_id):
    if not _validate_token(token, user_id):
        abort(404)

    req_json = request.get_json()
    food = Food()
    food.user_id = user_id
    food.receive_date = datetime.fromordinal(req_json['created'])
    food.calcium = req_json['calcium']
    food.calciumUnit = req_json['calciumUnit']
    food.calories = req_json['calories']
    food.carbs = req_json['carbs']
    food.carbsUnit = req_json['carbsUnit']
    food.description = req_json['description']
    food.fiber = req_json['fiber']
    food.fiberUnit = req_json['fiberUnit']
    food.folate = req_json['folate']
    food.folateUnit = req_json['folateUnit']
    food.glycemic_index = req_json['glycemicIndex']
    food.iron = req_json['iron']
    food.ironUnit = req_json['ironUnit']
    food.magnesium = req_json['magnesium']
    food.magnesiumUnit = req_json['magnesiumUnit']
    food.measurement = req_json['measurement']
    food.monounsaturated_fat = req_json['monounsaturatedFat']
    food.monounsaturated_fatUnit = req_json['monounsaturatedFatUnit']
    food.name = req_json['name']
    food.niacin = req_json['niacin']
    food.niacinUnit = req_json['niacinUnit']
    food.phosphorus = req_json['phosphorus']
    food.phosphorusUnit = req_json['phosphorusUnit']
    food.polyunsaturated_fat = req_json['polyunsaturatedFat']
    food.polyunsaturated_fatUnit = req_json['polyunsaturatedFatUnit']
    food.potassium = req_json['potassium']
    food.potassiumUnit = req_json['potassiumUnit']
    food.protein = req_json['protein']
    food.proteinUnit = req_json['proteinUnit']
    food.quantity = req_json['quantity']
    food.riboflavin = req_json['riboflavin']
    food.riboflavinUnit = req_json['riboflavinUnit']
    food.saturated_fat = req_json['saturatedFat']
    food.saturated_fatUnit = req_json['saturatedFatUnit']
    food.sodium = req_json['sodium']
    food.sodiumUnit = req_json['sodiumUnit']
    food.sugar = req_json['sugar']
    food.sugarUnit = req_json['sugarUnit']
    food.thiamin = req_json['thiamin']
    food.thiaminUnit = req_json['thiaminUnit']
    food.total_fat = req_json['totalFat']
    food.total_fatUnit = req_json['totalFatUnit']
    food.vitamin_a = req_json['vitaminA']
    food.vitamin_aUnit = req_json['vitaminAUnit']
    food.vitamin_b6 = req_json['vitaminB6']
    food.vitamin_b6Unit = req_json['vitaminB6Unit']
    food.vitamin_c = req_json['vitaminC']
    food.vitamin_cUnit = req_json['vitaminCUnit']
    food.vitamin_e = req_json['vitaminE']
    food.vitamin_eUnit = req_json['vitaminEUnit']
    food.vitamin_k = req_json['vitaminK']
    food.vitamin_kUnit = req_json['vitaminKUnit']
    food.zinc = req_json['zinc']
    food.zincUnit = req_json['zincUnit']

    db.session.add(food)
    db.session.commit()

    return '', 204


@api.route('/insulin', methods=['POST'])
def save_insulin(token, user_id):
    if not _validate_token(token, user_id):
        abort(404)

    req_json = request.get_json()
    insulin = InsulinDose()
    insulin.user_id = user_id
    insulin.receive_date = datetime.fromordinal(req_json['created'])
    insulin.units = req_json['units']
    insulin.unit_type = req_json['unitType']
    insulin.insulin_type = req_json['insulinType']

    db.session.add(insulin)
    db.session.commit()

    return '', 204


@api.route('/glucose', methods=['POST'])
def save_glucose(token, user_id):
    if not _validate_token(token, user_id):
        abort(404)

    req_json = request.get_json()
    bg = BgReading()
    bg.user_id = user_id
    bg.receive_date = datetime.fromordinal(req_json['created'])
    bg.value = req_json['calculated_value']

    db.session.add(bg)
    db.session.commit()

    return '', 204


def _validate_token(token, user_id):
    try:
        salt = token[:29]
        user_token = token[29:]

        serializer = URLSafeSerializer(config['TOKEN_SECRET_KEY'])
        user = User.query.get(user_id)

        return user_token == serializer.dumps(user.email, salt=salt)
    except:
        return False
