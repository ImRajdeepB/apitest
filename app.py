from flask import Flask, session, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
import os
import json
from marshmallow import Schema, fields, pprint
from sqlalchemy import func

app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Mapping(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), primary_key=True)
    place_name = db.Column(db.String(120), nullable=False)
    admin_name1 = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    accuracy = db.Column(db.Integer(), nullable=True)

    def __init__(self, key, place_name, admin_name1, latitude, longitude, accuracy):
        self.key = key
        self.place_name = place_name
        self.admin_name1 = admin_name1
        self.latitude = latitude
        self.longitude = longitude
        self.accuracy = accuracy

    def __repr__(self):
        return '<Place %r>' % self.place_name

    def approx(self, latitude, longitude):
        return (round(latitude, 2), round(longitude, 2))


class MappingSchema(Schema):
    class Meta:
        fields = ('key', 'place_name', 'admin_name1',
                  'latitude', 'longitude', 'accuracy')


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/api', methods=['GET'])
def get_all():
    resp = []
    # for u in db.session.query(Mapping).all():
    for u in Mapping.query.all():
        resp.append(u.__dict__)
        td = dict(u.__dict__)

    for r in resp:
        del r['_sa_instance_state']

    return jsonify(resp)


@app.route('/api/post_location', methods=['GET', 'POST'])
def post_location():
    key = request.json['key']
    place_name = request.json['place_name']
    admin_name1 = request.json['admin_name1']
    latitude = request.json['latitude']
    longitude = request.json['longitude']
    accuracy = request.json['accuracy']
    latR = round(latitude, 2)
    lonR = round(longitude, 2)

    try:
        new_mp = Mapping(key, place_name, admin_name1,
                         latitude, longitude, accuracy)
    except:
        return 'This location already exists'

    db.session.add(new_mp)
    db.session.commit()

    return jsonify(new_mp)


@app.route('/api/get_using_postgres', methods=['GET'])
def get_using_postgres():
    try:
        lat = float(request.args.get('latitude'))
        lon = float(request.args.get('longitude'))
    except:
        return 'Please provide latitude and longitude'
    req_loc = func.earth_box(func.ll_to_earth(lat, lon), 5000)
    loc_company = func.ll_to_earth(Mapping.latitude, Mapping.longitude)
    print(loc_company)
    result = Mapping.query.filter(req_loc.op("@>")(loc_company))
    print(result)
    mp_schema = MappingSchema(many=True)
    print(mp_schema)
    output = mp_schema.dump(result).data
    print(output)
    return jsonify(output)


@app.route('/api/get_using_self', methods=['GET'])
def get_using_self():
    pass


if __name__ == '__main__':
    app.run()
