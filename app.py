from flask import Flask, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm.attributes import QueryableAttribute
import os
import json
from marshmallow import Schema, fields, pprint


app = Flask(__name__)
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/mydb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# from models import Result
# from models import Zips


# class BaseModel(db.Model):
#     __abstract__ = True

#     def to_dict(self, show=None, _hide=[], _path=None):
#         """Return a dictionary representation of this model."""

#         show = show or []

#         hidden = self._hidden_fields if hasattr(self, "_hidden_fields") else []
#         default = self._default_fields if hasattr(
#             self, "_default_fields") else []
#         default.extend(['id', 'modified_at', 'created_at'])

#         if not _path:
#             _path = self.__tablename__.lower()

#             def prepend_path(item):
#                 item = item.lower()
#                 if item.split(".", 1)[0] == _path:
#                     return item
#                 if len(item) == 0:
#                     return item
#                 if item[0] != ".":
#                     item = ".%s" % item
#                 item = "%s%s" % (_path, item)
#                 return item

#             _hide[:] = [prepend_path(x) for x in _hide]
#             show[:] = [prepend_path(x) for x in show]

#         columns = self.__table__.columns.keys()
#         relationships = self.__mapper__.relationships.keys()
#         properties = dir(self)

#         ret_data = {}

#         for key in columns:
#             if key.startswith("_"):
#                 continue
#             check = "%s.%s" % (_path, key)
#             if check in _hide or key in hidden:
#                 continue
#             if check in show or key in default:
#                 ret_data[key] = getattr(self, key)

#         for key in relationships:
#             if key.startswith("_"):
#                 continue
#             check = "%s.%s" % (_path, key)
#             if check in _hide or key in hidden:
#                 continue
#             if check in show or key in default:
#                 _hide.append(check)
#                 is_list = self.__mapper__.relationships[key].uselist
#                 if is_list:
#                     items = getattr(self, key)
#                     if self.__mapper__.relationships[key].query_class is not None:
#                         if hasattr(items, "all"):
#                             items = items.all()
#                     ret_data[key] = []
#                     for item in items:
#                         ret_data[key].append(
#                             item.to_dict(
#                                 show=list(show),
#                                 _hide=list(_hide),
#                                 _path=("%s.%s" % (_path, key.lower())),
#                             )
#                         )
#                 else:
#                     if (
#                         self.__mapper__.relationships[key].query_class is not None
#                         or self.__mapper__.relationships[key].instrument_class
#                         is not None
#                     ):
#                         item = getattr(self, key)
#                         if item is not None:
#                             ret_data[key] = item.to_dict(
#                                 show=list(show),
#                                 _hide=list(_hide),
#                                 _path=("%s.%s" % (_path, key.lower())),
#                             )
#                         else:
#                             ret_data[key] = None
#                     else:
#                         ret_data[key] = getattr(self, key)

#         for key in list(set(properties) - set(columns) - set(relationships)):
#             if key.startswith("_"):
#                 continue
#             if not hasattr(self.__class__, key):
#                 continue
#             attr = getattr(self.__class__, key)
#             if not (isinstance(attr, property) or isinstance(attr, QueryableAttribute)):
#                 continue
#             check = "%s.%s" % (_path, key)
#             if check in _hide or key in hidden:
#                 continue
#             if check in show or key in default:
#                 val = getattr(self, key)
#                 if hasattr(val, "to_dict"):
#                     ret_data[key] = val.to_dict(
#                         show=list(show),
#                         _hide=list(_hide), _path=("%s.%s" % (_path, key.lower()))
#                         _path=("%s.%s" % (path, key.lower())),
#                     )
#                 else:
#                     try:
#                         ret_data[key] = json.loads(json.dumps(val))
#                     except:
#                         pass

#         return ret_data


class Mapping(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(), primary_key=True)
    place_name = db.Column(db.String(120), nullable=False)
    admin_name1 = db.Column(db.String(80), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    accuracy = db.Column(db.Integer(), nullable=True)

    def __repr__(self):
        return '<Place %r>' % self.place_name


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


@app.route('/')
def hello():
    return "Hello World!"


# @app.route('/<name>')
# def hello_name(name):
#     return "Hello {}!".format(name)

@app.route('/api')
def place():
    # return jsonify(json_list=Mapping.query.all())
    # print(Mapping.query.all())
    # return Mapping.query.all()
    resp = []
    # for u in db.session.query(Mapping).all():
    for u in Mapping.query.all():
        resp.append(u.__dict__)
        td = dict(u.__dict__)
        # print(json.dumps(u.__dict__))
        # print(td.pop('_sa_instance_state', None))
        # print(td)
    # print(json.dumps(resp))
    for r in resp:
        del r['_sa_instance_state']
    print(resp)
    return (jsonify(resp))


@app.route('/post_location', methods=['GET', 'POST'])
def post_location():
    pass


if __name__ == '__main__':
    app.run()
