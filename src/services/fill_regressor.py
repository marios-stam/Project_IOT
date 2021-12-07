import numpy as np
from src.utils.utils import rand_perc


def rand_history(fill_lvl=85):
    base_rate = 2.5 + (1 * rand_perc(center=True))
    res = [0]
    while res[-1] < 100:
        res.append(res[-1] + base_rate * (1 + 0.25*rand_perc(center=True)))
    res[-1] = 100
    return res


def get_sensor_history(sensor_id):
    return rand_history()

