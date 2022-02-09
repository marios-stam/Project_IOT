from flask import make_response
from ..models import db, Regression
from flask import jsonify
from datetime import datetime
from .fill_regressor import fill_regressor as fr
from ..utils import diff_time
from ..__config__ import REFRESH_INTERVAL, NUM_MEASUREMENTS


def get_angle(sensor_id):
    result = db.session.query(Regression).filter(Regression.sensor_id == sensor_id).all()

    if len(result) > 0:
        print(f"Gettind data of bin: {sensor_id} ...")
        data = result[0].__dict__
        print(data)
        data.pop('_sa_instance_state')

        t1 = datetime.strptime(data['timestamp'][:-4], '%Y-%m-%d %H:%M:%S')
        delay = diff_time(t1, datetime.now())
    if len(result) <= 0 or delay > REFRESH_INTERVAL:
        data = {
            'sensor_id': sensor_id,
            'angle': fr(sensor_id, NUM_MEASUREMENTS),
            'timestamp': datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        }
    if len(result) <= 0:
        # Create new DB entry for the sensor with the above data
        pass
    else:
        # Update existon entry with the above angle
        pass

    return make_response(jsonify(data))
