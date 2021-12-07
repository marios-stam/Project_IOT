from matplotlib import pyplot as plt
from src.services.fill_regressor import *


def graph_history(sensor_id=None, rep=1):
    for i in range(rep):
        tmp = get_sensor_history(sensor_id)
        plt.plot(tmp)
    plt.show()