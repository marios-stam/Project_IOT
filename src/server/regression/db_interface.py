from flask import make_response
from ..models import db, Regression
from flask import request, jsonify
import requests


def get_angle(sensor_id):

    result = db.session.query(Regression).filter(Regression.sensor_id == sensor_id).all()
    if len(result) == 0:
        return make_response(f"No sensor found!")
    else:
        print(f"Gettind data of bin: {sensor_id} ...")
        data = result[0].__dict__
        print(data)
        data.pop('_sa_instance_state')

    return make_response(jsonify(data))
