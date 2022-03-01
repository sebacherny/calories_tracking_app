import requests
import unittest
import json
import MySQLdb
import os

DB_TEST_HOST = "localhost"
DB_TEST_USER = "root"
DB_TEST_PASSWORD = "root"
DB_TEST_NAME = "calories_db"

BASE_URL = "http://localhost:8080"

class ApiTests(unittest.TestCase):
    
    def test_complete_process(self):
        r = requests.get(BASE_URL + "/api/foods")
        self.assertEqual(r.json(), {'message': 'Missing header in request'})
        self.assertEqual(r.status_code, 401)
        r = requests.get(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456"})
        self.assertEqual(r.json(), {'message': 'Unauthorized'})
        self.assertEqual(r.status_code, 401)
        
        r = requests.get(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer admin-token-123"})
        self.assertEqual(r.json(), [])
        self.assertEqual(r.status_code, 200)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Apple",
                                 "date_eaten":"2022-02-27 08:37:00",
                                 "calories": 50,
                                 "price": 1}))
        self.assertEqual(r.json(), {"id": 1})
        self.assertEqual(r.status_code, 200)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-789",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Banana",
                                 "date_eaten":"2022-02-25 10:00:00",
                                 "calories": 50,
                                 "price": 1}))
        self.assertEqual(r.json(), {"id": 2})
        self.assertEqual(r.status_code, 200)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Juice",
                                 "date_eaten":"2022-02-27 08:37:00",
                                 "calories": 50,
                                 "price": 1.3})
                         )
        self.assertEqual(r.json(), {"id": 3})
        self.assertEqual(r.status_code, 200)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Juice",
                                 "date_eaten":"2022-02-27 08:37:00",
                                 "calories": 50})
                         )
        self.assertEqual(r.json(), {"id": 4})
        self.assertEqual(r.status_code, 200)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "",
                                 "date_eaten":"2022-02-27 08:37:00",
                                 "calories": 50,
                                 "price": 1})
                         )
        self.assertEqual(r.json(), {"message": "Food's name missing"})
        self.assertEqual(r.status_code, 400)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"calories": 2})
                         )
        self.assertEqual(r.json(), {"message": "Food's name missing"})
        self.assertEqual(r.status_code, 400)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Apple",
                                 "date_eaten":"2022-27-27 08:37:00",
                                 "calories": 50,
                                 "price": 1})
                         )
        self.assertEqual(r.json(), {"message": "Date missing or bad format"})
        self.assertEqual(r.status_code, 400)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Apple",
                                 "date_eaten":"2022-2-27 08:37:00",
                                 "calories": "calories",
                                 "price": 1})
                         )
        self.assertEqual(r.json(), {"message": "Calories must be a positive integer"})
        self.assertEqual(r.status_code, 400)
        
        r = requests.post(BASE_URL + "/api/foods",
                         headers={"Authorization": "Bearer user-token-456",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Apple",
                                 "date_eaten":"2022-2-27 08:37:00",
                                 "calories": 50,
                                 "price": "price"})
                         )
        self.assertEqual(r.json(), {"message": "Price must be either empty or a positive number"})
        self.assertEqual(r.status_code, 400)
        
        r = requests.get(BASE_URL + "/api/user/2/foods",
                         headers={"Authorization": "Bearer user-token-456"})
        self.assertEqual(r.json(), [{"id": "1",
                                     "name": "Apple",
                                     "date_eaten": "2022-02-27 08:37:00",
                                     "calories": "50",
                                     "price": "1.0",
                                     "user_id": "2"},
                                     {"id": "3", "name": "Juice",
                                      "date_eaten": "2022-02-27 08:37:00",
                                      "calories": "50", "price": "1.3",
                                      "user_id": "2"},
                                     {"id": "4", "name": "Juice",
                                      "date_eaten": "2022-02-27 08:37:00",
                                      "calories": "50", "price": "",
                                      "user_id": "2"}])
        self.assertEqual(r.status_code, 200)
        
        r = requests.get(BASE_URL + "/api/user/2/foods",
                         headers={"Authorization": "Bearer user-token-789"})
        self.assertEqual(r.json(), {"message": "Unauthorized, it's not your food"})
        self.assertEqual(r.status_code, 401)
        
        r = requests.get(BASE_URL + "/api/user/2/foods",
                         headers={"Authorization": "Bearer bad token"})
        self.assertEqual(r.json(), {"message": "Auth header must contain bearer followed by token"})
        self.assertEqual(r.status_code, 401)
        
        r = requests.get(BASE_URL + "/api/user/2/foods",
                         headers={"Authorization": "Bearer bad_token"})
        self.assertEqual(r.json(), {"message": "Token is invalid !!"})
        self.assertEqual(r.status_code, 401)
        
        r = requests.get(BASE_URL + "/api/foods/1",
                         headers={"Authorization": "Bearer user-token-456"})
        self.assertEqual(r.json(), {"id": "1", "name": "Apple",
                                    "date_eaten": "2022-02-27 08:37:00",
                                    "calories": "50", "price": "1.0",
                                    "user_id": "2"})
        self.assertEqual(r.status_code, 200)
        
        r = requests.get(BASE_URL + "/api/foods/1",
                         headers={"Authorization": "Bearer user-token-789"})
        self.assertEqual(r.json(), {"message": "Unauthorized, it's not your food"})
        self.assertEqual(r.status_code, 401)
        
        r = requests.delete(BASE_URL + "/api/foods/1",
                         headers={"Authorization": "Bearer user-token-456"})
        self.assertEqual(r.json(), {"message": "Unauthorized"})
        self.assertEqual(r.status_code, 401)
        
        r = requests.delete(BASE_URL + "/api/foods/1",
                         headers={"Authorization": "Bearer admin-token-123"})
        self.assertEqual(r.json(), {"deleted": True})
        self.assertEqual(r.status_code, 200)
        
        r = requests.put(BASE_URL + "/api/foods/1",
                         headers={"Authorization": "Bearer admin-token-123",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Watermelon, not banana",
                                          "date_eaten":"2022-02-28 08:37:00",
                                          "calories": 40,
                                          "price": 1}))
        self.assertEqual(r.json(), {'message': 'Unexistent entry'})
        self.assertEqual(r.status_code, 400)
        
        r = requests.put(BASE_URL + "/api/foods/2",
                         headers={"Authorization": "Bearer admin-token-123",
                                  "Content-Type": "application/json"},
                         data=json.dumps({"name": "Watermelon, not banana",
                                          "date_eaten":"2022-02-28 08:37:00",
                                          "calories": 40,
                                          "price": 1}))
        self.assertEqual(r.json(), {"id": "2",
                                    "name": "Watermelon, not banana",
                                    "date_eaten": "2022-02-28 08:37:00",
                                    "calories": "40", "price": "1.0",
                                    "user_id": "3"})
        self.assertEqual(r.status_code, 200)
        
        
        

if __name__ == "__main__":
    SQL_FILE = os.path.dirname(os.path.realpath(__file__))  + "/../../main/files/migrations/migration_001.sql"
    command = """mysql -u %s -p"%s" --host %s  < %s""" % (
        DB_TEST_USER, DB_TEST_PASSWORD, DB_TEST_HOST, SQL_FILE)
    os.system(command)
    unittest.main()
