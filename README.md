# apitest

## Usage

```
$ psql mydb
mydb=# CREATE EXTENSION cube;
mydb=# CREATE EXTENSION earthdistance;
```

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export FLASK_ENV=development
$ python app.py
```

## Endpoints

### Create Location

`POST /api/post_location`

Example request body:

```json
{
  "accuracy": null,
  "admin_name1": "San Andreas",
  "key": "IN/200003",
  "latitude": 25.5,
  "longitude": 71.4,
  "place_name": "San Fierro"
}
```

### Get Places within 5km (earthdistance)

`GET /api/get_using_postgres`

Returns an array of places within 5km radius of queried point using postgres earthdistance extension.

Query Parameters:

`?latitude=28.6333&longitude=77.2167`
