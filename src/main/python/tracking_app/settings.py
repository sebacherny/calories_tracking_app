import os

MAIN_BASE_DIR = os.path.dirname(os.path.realpath(__file__))  + "/../.."

HARDCODED_USERS = [
    {"user": "admin", "token": "admin-token-123", "id": 1, "is_admin": True,
     "calories_daily_limit": 2100, "price_monthly_limit": 1000},
    {"user": "not_admin_1", "token": "user-token-456", "id": 2, "is_admin": False,
     "calories_daily_limit": 2100, "price_monthly_limit": 1000},
    {"user": "common_user_2", "token": "user-token-789", "id": 3, "is_admin": False,
     "calories_daily_limit": 2100, "price_monthly_limit": 1000},
]