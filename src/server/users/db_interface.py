from flask import Blueprint, make_response
from flask import current_app as app
from flask.json import _dump_arg_defaults
from ..models import db, User
from datetime import datetime as dt
from flask import request, jsonify


def get_user(user_id=None):
    result = db.session.query(User).filter(User.id == user_id).all()
    if(len(result) == 0):
        return make_response(f"No user found with ID: {user_id}")
    else:
        print(f"Gettind data of user: {user_id} ...")
        data = result[0].__dict__
        data.pop('_sa_instance_state')

        data_json = jsonify(data)

        return make_response(data_json)


def update_user(user_id=None):
    data = request.get_json()
    id = data['id']
    result = db.session.query(User).filter(User.id == id).all()
    if(len(result) == 0):
        return create_user(data)

    print(f"Updating user with ID:{id} ...")
    for key, value in data.items():
        if key == 'created' or key == 'updated':
            result[0].updated = dt.now()
            continue

        setattr(result[0], key, value)

    db.session.commit()

    return make_response("PUT called")


def create_user(data=None):
    if data == None:
        data = request.get_json()

    data['created'] = dt.now()  # set created date
    new_user = User(**data)

    # add to database
    db.session.add(new_user)
    db.session.commit()
    return make_response("POST called")
