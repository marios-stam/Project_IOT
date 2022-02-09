from ..bins.db_interface import get_bin_history
from datetime import datetime
from ..utils import diff_time


def fill_regressor(sensor_id, iters=150):
    counter = 0
    sum = 0
    start_time = None

    data = get_bin_history(sensor_id, iters)[::-1]
    for d in data:
        if d['fill_level'] < 0.01 or start_time is None:
            start_time = datetime.strptime(d['timestamp'][:-4], '%Y-%m-%d %H:%M:%S')
            continue

        if d['fill_level'] > 0.99:
            continue

        sum += d['fill_level'] / diff_time(start_time, datetime.strptime(d['timestamp'][:-4], '%Y-%m-%d %H:%M:%S'))
        counter += 1

    return sum / counter
