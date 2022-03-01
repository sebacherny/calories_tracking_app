from bottle import Bottle, run, template, request, response
import bottle
import json
from database_utils import get_all_food_entries, \
    get_user_limits_from_db, get_all_users_info_from_db
import datetime
from collections import defaultdict
import os
import settings
from rest_api_requests import api_app, serialize_food_entries, token_required

main_app = Bottle()

@main_app.route('/hello')
def hello():
    return "Hello World!"

@main_app.route('/main')
@token_required
def first_page(current_user):
    is_admin = current_user["is_admin"]
    user_id = current_user["id"]

    all_food_entries = list(get_all_food_entries(None if is_admin else current_user["id"]))
    admin_report = _get_admin_report(all_food_entries) if is_admin else None
    all_food_entries = serialize_food_entries(all_food_entries)
    user_limits = get_user_limits_from_db(user_id)
    all_users = get_all_users_info_from_db() if is_admin else None
    return template("main_page.tmpl", is_admin=is_admin,
                    food_entries=all_food_entries,
                    admin_report=admin_report,
                    calories_daily_limit=user_limits["calories_daily_limit"],
                    price_monthly_limit=user_limits["price_monthly_limit"],
                    all_users=all_users)


def _get_admin_report(all_food_entries):
    last_week_entries = [entry for entry in all_food_entries
                         if _time_difference_from_now_is_between(entry, 0, 7)]
    return {
        "added_entries_last_7_days": len(last_week_entries),
        "added_entries_previous_week": len([entry for entry in all_food_entries
                                            if _time_difference_from_now_is_between(entry, 7, 14)]),
        "average_calories_per_user_last_week": _get_average_calories_from_entries(last_week_entries)
    }

def _time_difference_from_now_is_between(entry, days_min, days_max):
    dt_now = datetime.datetime.now()
    last_dt_allowed = dt_now - datetime.timedelta(days_min)
    first_dt_allowed = dt_now - datetime.timedelta(days_max)
    dt_entry = entry["date_eaten"]
    #datetime.datetime.strptime(entry["date_eaten"], "%Y-%m-%d %H:%M:%S")
    return dt_entry >= first_dt_allowed and dt_entry < last_dt_allowed

def _get_average_calories_from_entries(food_entries):
    if not food_entries:
        return 0
    total_amount_of_calories = sum(entry["calories"] for entry in food_entries)
    distinct_users = len(set(entry["user_id"] for entry in food_entries))
    return total_amount_of_calories/distinct_users



if __name__ == "__main__":
    bottle.TEMPLATE_PATH.append(settings.MAIN_BASE_DIR + '/files/templates')
    main_app.merge(api_app)
    run(main_app, host='localhost', port=8080, debug=True)