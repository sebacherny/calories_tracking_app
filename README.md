## Description

This project tracks the calories and money spent by users in food.

It warns the user when their daily calories' limit is about to be reached, as well as the monthly money limit.

## Local installation and running

To run locally, I performed the following in a Linux computer:

Being in folder calories_tracking_bottle:

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
mysql -uroot -proot < calories_tracking_bottle/src/main/files/migrations/migration_001.sql
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
curl http://localhost:8080/api/foods?token=admin-token-123
```

POST /api/foods:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "Apple", "date_eaten":"2022-02-27 08:37:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods?token=user-token-456

curl -X POST -H "Content-Type: application/json" -d '{"name": "Banana", "date_eaten":"2022-02-25 10:00:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods?token=user-token-789

curl -X POST -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-02-27 08:37:00", "calories": 50, "price": 1.3}' http://localhost:8080/api/foods?token=user-token-456

curl -X POST -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-02-27 08:37:00", "calories": 50}' http://localhost:8080/api/foods?token=user-token-456


```

Posts with bad body:
```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "", "date_eaten":"2022-02-27 08:37:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods?token=user-token-456

curl -X POST -H "Content-Type: application/json" -d '{"price": 1}' http://localhost:8080/api/foods?token=user-token-456

curl -X POST -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-2-27 08:37:00", "calories": 50, "price": 1}' http://localhost:8080/api/foods?token=user-token-456

curl -X POST -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-02-27 08:37:00", "calories": "calories", "price": 1}' http://localhost:8080/api/foods?token=user-token-456

curl -X POST -H "Content-Type: application/json" -d '{"name": "Juice", "date_eaten":"2022-02-27 08:37:00", "calories": 10, "price": "price"}' http://localhost:8080/api/foods?token=user-token-456
```

--

GET /api/user/:user_id/foods
```bash
curl http://localhost:8080/api/user/2/foods?token=user-token-456
```

GET without permission:
```bash
curl http://localhost:8080/api/user/2/foods?token=user-token-789
curl http://localhost:8080/api/user/2/foods?token=bad-token
```

GET /api/foods/:entry_id
```bash
curl http://localhost:8080/api/foods/1?token=user-token-456
```

GET without permission:
```bash
curl http://localhost:8080/api/foods/1?token=user-token-789
```

DELETE /api/foods/:entry_id

Without permission
```bash
curl -X DELETE http://localhost:8080/api/foods/1?token=user-token-456
```

With permission
```bash
curl -X DELETE http://localhost:8080/api/foods/1?token=admin-token-123
```


PUT /api/foods/:entry_id

Without permission
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Watermelon, not banada", "date_eaten":"2022-02-28 08:37:00", "calories": 40, "price": 1' http://localhost:8080/api/foods/2?token=user-token-789
```


With permission
```bash
curl -X PUT -H "Content-Type: application/json" -d '{"name": "Watermelon, not banada", "date_eaten":"2022-02-28 08:37:00", "calories": 40, "price": 1}' http://localhost:8080/api/foods/2?token=admin-token-123
```


