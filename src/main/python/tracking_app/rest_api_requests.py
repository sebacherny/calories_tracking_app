from bottle import Bottle, run, template, request, response
from database_utils import create_food_entry, get_all_food_entries, \
    delete_food_entry_from_db, update_db_food_entry, \
    get_user_limits_from_db, get_username_and_hashed_password, \
    get_db_food_entry, get_user_info_from_db_if_exists
import json
from functools import wraps
import settings
import datetime

api_app = Bottle()

def token_required(f, must_be_admin=False):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # if 'x-access-token' in request.headers:
        #     token = request.headers['x-access-token']
        token = request.params.get("token")
        # return 401 if token is not passed
        if not token:
            response.content_type = "application/json"
            response.status = 401
            return json.dumps({'message' : 'Token is missing !!'})
        try:
            current_user = [x for x in settings.HARDCODED_USERS
                            if x["token"] == token][0]
            if must_be_admin and not current_user["is_admin"]:
                response.content_type = "application/json"
                response.status = 401
                return json.dumps({
                    'message' : 'Unauthorized'
                })
        except Exception as e:
            print(e)
            response.content_type = "application/json"
            response.status = 401
            return json.dumps({
                'message' : 'Token is invalid !!'
            })
        return f(current_user, *args, **kwargs)

    return decorated

def admin_token_required(f):
    return token_required(f, True)


def _serialize_db_val(v):
    if v is None:
        return ""
    return str(v)

def _serialize_db_json(x):
    return {k: _serialize_db_val(v) for k, v in x.items()}

@api_app.route('/api/foods')
@admin_token_required
def api_get_all_food_entries(current_user):
    response.content_type = "application/json"
    # response.status = response_status
    return json.dumps(serialize_food_entries(get_all_food_entries()))

def serialize_food_entries(entries):
    return [_serialize_db_json(x) for x in entries]

@api_app.route('/api/user/<user_id>/foods')
@token_required
def api_get_all_food_entries_for_user(current_user, user_id):
    response.content_type = "application/json"
    if (not current_user["is_admin"]) and current_user["id"] != int(user_id):
        response.status = 401
        return {"message": "Unauthorized, it's not your food"}
    return json.dumps(serialize_food_entries(get_all_food_entries(user_id)))

@api_app.route('/api/foods/<entry_id>')
@token_required
def api_get_all_food_entries_for_user(current_user, entry_id):
    response.content_type = "application/json"
    entry_info = get_db_food_entry(entry_id)
    if not entry_info:
        response.status = 401
        return {"message": "Food entry unexistent"}
    if (not current_user["is_admin"]) and current_user["id"] != entry_info["user_id"]:
        response.status = 401
        return {"message": "Unauthorized, it's not your food"}
    return json.dumps(serialize_food_entries([entry_info])[0])

def is_date_good_format(date_text):
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
        return True
    except ValueError:
        return False

@api_app.post('/api/foods')
@token_required
def create_new_food_entry(current_user):
    req_json = json.loads(request.body.read())
    food_user_id = int(req_json.get("user_id") or current_user["id"])
    if (not current_user["is_admin"]) and food_user_id != current_user["id"]:
        response.content_type = "application/json"
        response.status = 401
        return {"message": "Unauthorized, it's not your food"}
    if not get_user_info_from_db_if_exists(food_user_id):
        response.content_type = "application/json"
        response.status = 404
        return {"message": "User not found"}
    if not req_json.get("name"):
        response.content_type = "application/json"
        response.status = 400
        return {"message": "Food's name missing"}
    if not req_json.get("date_eaten") or not is_date_good_format(req_json["date_eaten"]):
        response.content_type = "application/json"
        response.status = 400
        return {"message": "Date missing or bad format"}
    if not req_json.get("calories") or not isinstance(req_json["calories"], int) or int(req_json["calories"]) <= 0:
        response.content_type = "application/json"
        response.status = 400
        return {"message": "Calories must be a positive integer"}
    if req_json.get("price") and (not isinstance(req_json.get("price"), float) or float(req_json.get("price")) <= 0):
        response.content_type = "application/json"
        response.status = 400
        return {"message": "Price must be either empty or a positive number"}
    new_food_entry_id = create_food_entry(req_json["name"],
                                       req_json["date_eaten"],
                                       req_json["calories"],
                                       req_json.get("price") or 0,
                                       food_user_id,
                                       )
    response.content_type = "application/json"
    return json.dumps({"id": new_food_entry_id})

@api_app.delete('/api/foods/<entry_id>')
@admin_token_required
def delete_food_entry(current_user, entry_id):
    # XXX: Should check it exists ?
    delete_food_entry_from_db(entry_id)
    response.content_type = "application/json"
    return json.dumps({"deleted": True})


@api_app.put('/api/foods/<entry_id>')
@admin_token_required
def update_food_entry(current_user, entry_id):
    updated_food_entry = update_db_food_entry(entry_id, **json.loads(request.body.read()))
    response.content_type = "application/json"
    if updated_food_entry:
        return json.dumps(_serialize_db_json(updated_food_entry))
    else:
        # XXX: Should be 400 ?
        return {"message": "Unexistent entry"}