import MySQLdb
import settings

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "calories_db"

def get_database_connection():
    return MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD,
                           db=DB_NAME, charset="utf8")


def get_all_food_entries(user_id=None):
    query = 'SELECT id, name, date_eaten, calories, price, user_id from food '
    if user_id:
        query += ' where user_id = %s' % user_id
    try:
        conn = get_database_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query) # (user,))
        foods = cursor.fetchall()
        cursor.close()
    finally:
        conn.close()
    return foods

def create_food_entry(name, date_eaten, calories, price, user_id):
    query = 'INSERT into food (name, date_eaten, calories, price, user_id)'
    query += ' VALUES ("{}", "{}", {}, {}, {})'.format(name, date_eaten, calories, price or "null", user_id)
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        cursor.close()
        conn.commit()
    finally:
        conn.close()
    return cursor.lastrowid

def delete_food_entry_from_db(food_entry_id):
    query = 'DELETE from food where id = %s'
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute(query, (food_entry_id,))
        cursor.close()
        conn.commit()
    finally:
        conn.close()


def update_db_food_entry(entry_id, name=None, date_eaten=None, calories=None,
                         price=None, user_id=None):
    query = 'UPDATE food set '
    if name:
        query += 'name="{}", '.format(name)
    if date_eaten:
        query += 'date_eaten="{}", '.format(date_eaten)
    if calories:
        query += 'calories={}, '.format(calories)
    if price:
        query += 'price={}, '.format(price)
    if user_id:
        query += 'user_id={}, '.format(user_id)
    if query == 'UPDATE food set ':
        # No changes
        return get_db_food_entry(entry_id)
    query = query[:-2]
    query += ' where id = %s'
    try:
        conn = get_database_connection()
        cursor = conn.cursor()
        cursor.execute(query, (entry_id,))
        cursor.close()
        conn.commit()
    finally:
        conn.close()
    return get_db_food_entry(entry_id)

def get_db_food_entry(entry_id):
    query = 'SELECT id, name, date_eaten, calories, price, user_id from food where id = %s'
    try:
        conn = get_database_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (entry_id,))
        entry = cursor.fetchone()
        cursor.close()
    finally:
        conn.close()
    return entry

def get_user_info_from_db_if_exists(user_id):
    user = [u for u in settings.HARDCODED_USERS if u["id"] == user_id]
    if user:
        return user[0]
    return None

def get_user_limits_from_db(user_id):
    user = [u for u in settings.HARDCODED_USERS if u["id"] == user_id][0]
    return {
        "calories_daily_limit": user["calories_daily_limit"],
        "price_monthly_limit": user["price_monthly_limit"]
    }
    # query = 'SELECT calories_daily_limit, price_monthly_limit from user where id = %s'
    # try:
    #     conn = get_database_connection()
    #     cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    #     cursor.execute(query, (user_id,)) # (user,))
    #     user_limits = cursor.fetchone()
    #     cursor.close()
    # finally:
    #     conn.close()
    # return user_limits

def get_all_users_info_from_db():
    return {u["id"]: {"calories_daily_limit": u["calories_daily_limit"],
                      "price_monthly_limit": u["price_monthly_limit"]} for u in settings.HARDCODED_USERS}

def get_username_and_hashed_password(user_id):
    query = 'SELECT username, password from user where id = %s'
    try:
        conn = get_database_connection()
        cursor = conn.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(query, (user_id,)) # (user,))
        user_info = cursor.fetchone()
        cursor.close()
        return user_info
    finally:
        conn.close()
    return user_info