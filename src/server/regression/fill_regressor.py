from tracemalloc import start
from ..bins.db_interface import get_bin_history
from datetime import datetime
from ..utils import diff_time


def fill_regressor(sensor_id, iters=150):
    counter = 0
    sum = 0
    prev_time = None
    prev = None

    data = get_bin_history(sensor_id, iters).json
    for d in data:

        if d['fill_level'] > 0.99:
            continue

        if not (d['fill_level'] < 0.01 or prev_time is None or prev is None):
            ang = (d['fill_level'] - prev) / (d['time_online'] - prev_time)
            sum += ang
            counter += 1

        prev = d['fill_level']
        prev_time = d['time_online']

    return sum / counter
