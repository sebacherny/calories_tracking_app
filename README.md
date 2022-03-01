## Description

This project tracks the calories and money spent by users in food.

It warns the user when their daily calories' limit is about to be reached, as well as the monthly money limit.

## Local installation and running

To run locally, I performed the following in a Linux computer:

Being in folder calories_tracking:

```bash
python3.8 -m venv env

source env/bin/activate

python3.8 -m pip install -r requirements.txt

```

And to run the project:

```bash
python3.8 src/main/python/tracking_app/main.py
```

## Database

The program communicates constantly with a database, to store food entries as well as users (users part not implemented).

To create it:

```bash
mysql -uroot -proot < src/main/files/migrations/migration_001.sql
```

## REST API

To test requsts from console, the code is currently expecting a token in the url. So to every request we should add "?token=<TOKEN>" .

## Endpoints

- /api/foods

	- GET: returns the complete list of food entries (required admin privilege)

	- POST: creates a food entry. Requires user token. With admin privileges the user_id may be set.

		- Example body for non-admin user:

```javascript
{"calories": 100, "price": 5, "date_eaten": "2022-02-28 10:00:00", "name": "Apple"}
```

		- Example body for admin user:

```javascript
{"calories": 100, "price": 5, "date_eaten": "2022-02-28 10:00:00", "name": "Apple", "user_id": 2}
```

		- Checks: Date must be in correct format and is required; calories must be a number and is required; name is required; user_id must be a valid user id.


- /api/user/:user_id/foods

	- GET: returns the complete list of food entries. Requires either admin privileges or to be user_id.

- /api/foods/:entry_id

	- GET: Returns info for this particular food entry. Requires either admin privileges or to be the user owner of this entry.

	- DELETE: Deletes the entry. Requires admin privileges.

	- PUT: Edits the entry. Requires admin priviliges. The body must similar to the POST in /api/foods .


## Testing endpoints commands:

GET /api/foods:

```bash
curl http://localhost:8080/api/foods -H "Authorization: Bearer admin-token-123"
```
```javascript
[]
```

POST /api/foods:

```bash
curl -X POST -H "Authorization: Bearer user-token-456" -H "Content-Type: application/json" -d '{"name": "Apple", "date_eaten":"2022-02-27 08:37:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods

```
```javascript
{"id": 1}
```

```bash
curl -X POST -H "Authorization: Bearer user-token-789" -H "Content-Type: application/json" -d '{"name": "Banana", "date_eaten":"2022-02-25 10:00:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods
```
```javascript
{"id": 2}
```

```bash
curl -X POST -H "Authorization: Bearer user-token-456" -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-02-27 08:37:00", "calories": 50, "price": 1.3}' http://localhost:8080/api/foods
```
```javascript
{"id": 3}
```

```bash
curl -X POST -H "Authorization: Bearer user-token-456" -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-02-27 08:37:00", "calories": 50}' http://localhost:8080/api/foods
```
```javascript
{"id": 4}
```

Post with bad token:
```bash
 curl -X POST -H "Content-Type: application/json" -d '{"name": "", "date_eaten":"2022-02-27 08:37:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods?token=user-token-456
```
```javascript
{"message": "Missing header in request"}
```

Posts with bad body:
```bash
curl -X POST -H "Authorization: Bearer user-token-456" -H "Content-Type: application/json" -d '{"name": "", "date_eaten":"2022-02-27 08:37:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods
```
```javascript
{"message": "Food's name missing"}
```

```bash
curl -X POST -H "Authorization: Bearer user-token-456" -H "Content-Type: application/json" -d '{"price": 1}' http://localhost:8080/api/foods
```
```javascript
{"message": "Food's name missing"}
```

```bash
curl -X POST -H "Authorization: Bearer user-token-456" -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-27-02 08:37:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods
```
```javascript
{"message": "Date missing or bad format"}
```


```bash
curl -X POST -H "Authorization: Bearer user-token-456" -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-02-27 08:37:00", "calories": "calories", "price": 1}' http://localhost:8080/api/foods
```
```javascript
{"message": "Calories must be a positive integer"}
```


```bash 
curl -X POST -H "Authorization: Bearer user-token-456" -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-02-27 08:37:00", "calories": 50, "price": "price"}' http://localhost:8080/api/foods
```
```javascript
{"message": "Price must be either empty or a positive number"}
```


--

GET /api/user/:user_id/foods
```bash
curl -H "Authorization: Bearer user-token-456" http://localhost:8080/api/user/2/foods
```
```javascript
[{"id": "1", "name": "Apple", "date_eaten": "2022-02-27 08:37:00", "calories": "50", "price": "1.0", "user_id": "2"}, {"id": "3", "name": "Juice", "date_eaten": "2022-02-27 08:37:00", "calories": "50", "price": "1.3", "user_id": "2"}, {"id": "4", "name": "Juice", "date_eaten": "2022-02-27 08:37:00", "calories": "50", "price": "", "user_id": "2"}]
```


GET without permission:
```bash
curl -H "Authorization: Bearer user-token-789" http://localhost:8080/api/user/2/foods
curl -H "Authorization: Bearer Bad token" http://localhost:8080/api/user/2/foods
curl -H "Authorization: Bearer Bad_token" http://localhost:8080/api/user/2/foods
```
```javascript
{"message": "Unauthorized, it's not your food"}
{"message": "Auth header must contain bearer followed by token"}
{"message": "Token is invalid !!"}
```


GET /api/foods/:entry_id
```bash
curl -H "Authorization: Bearer user-token-456" http://localhost:8080/api/foods/1
```
```javascript
{"id": "1", "name": "Apple", "date_eaten": "2022-02-27 08:37:00", "calories": "50", "price": "1.0", "user_id": "2"}
```


GET without permission:
```bash
curl -H "Authorization: Bearer user-token-789" http://localhost:8080/api/foods/1
```
```javascript
{"message": "Unauthorized, it's not your food"}
```


DELETE /api/foods/:entry_id

Without permission
```bash
curl -X DELETE -H "Authorization: Bearer user-token-456" http://localhost:8080/api/foods/1
```
```javascript
{"message": "Unauthorized"}
```


With permission
```bash
curl -X DELETE -H "Authorization: Bearer admin-token-123" http://localhost:8080/api/foods/1
```
```javascript
{"deleted": true}
```



PUT /api/foods/:entry_id

Without permission
```bash
curl -X PUT -H "Authorization: Bearer user-token-789" -H "Content-Type: application/json" -d '{"name": "Watermelon, not banada", "date_eaten":"2022-02-28 08:37:00", "calories": 40, "price": 1' http://localhost:8080/api/foods/2
```
```javascript
{"message": "Unauthorized"}
```



With permission
```bash
curl -X PUT -H "Authorization: Bearer admin-token-123" -H "Content-Type: application/json" -d '{"name": "Watermelon, not banana", "date_eaten":"2022-02-28 08:37:00", "calories": 40, "price": 1}' http://localhost:8080/api/foods/2
```
```javascript
{"id": "2", "name": "Watermelon, not banana", "date_eaten": "2022-02-28 08:37:00", "calories": "40", "price": "1.0", "user_id": "3"}
```


## Unittests

In folder src/test there is a unittest. It creates the SQL database from the migration, and after that runs the examples mentioned above, creating real food entries for differents users.

After running it, we can go to http://localhost:8080/main?token=admin-token-123 for example and see all the automatically added entries.

With the main.py running in another console:

```bash
source env/bin/activate

python3.8 src/test/python/tests_api_requests.py 
```

Output:
```bash
mysql: [Warning] Using a password on the command line interface can be insecure.
.
----------------------------------------------------------------------
Ran 1 test in 0.074s

OK
```

