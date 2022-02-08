from flask import make_response
from ..models import db, Regression
from flask import request, jsonify
from datetime import datetime
import requests
from ..fill_regressor import fill_regressor as fr
from ..utils import diff_time


def get_angle(sensor_id):
    result = db.session.query(Regression).filter(Regression.sensor_id == sensor_id).all()

    # Regression
    # refresh_interval = 6 * 60 * 60    # 6 hours
    refresh_interval = 5 * 60           # 5 minutes
    num_measurements = 150

    if len(result) > 0:
        print(f"Gettind data of bin: {sensor_id} ...")
        data = result[0].__dict__
        print(data)
        data.pop('_sa_instance_state')

        t1 = datetime.strptime(data['timestamp'][:-4], '%Y-%m-%d %H:%M:%S')
        delay = diff_time(t1, datetime.now())
    if len(result) <= 0 or delay > refresh_interval:
        fr(sensor_id, num_measurements)

    return make_response(jsonify(data))
