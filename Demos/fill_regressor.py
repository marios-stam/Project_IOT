from matplotlib import pyplot as plt
from src.server.utils import rand_history
from random import shuffle
from ..bins.db_interface import get_bin_history


def fill_regressor(sensor_id, iters=150, method="web"):
    n = 1
    counter = 0
    sum = 0

    if method == 'web':
        raw = get_bin_history(sensor_id, iters)
    elif method == 'sim':
        data = rand_history(id=sensor_id, hours=500)
    else:
        return

    for d in data:
        if d < 1:
            n = 1
            continue

        if d > 99:
            continue
        sum += (d / n)
        counter += 1
        n += 1

    return sum / counter


def evaluator():
    ids = list(range(36))
    shuffle(ids)
    f = plt.figure(figsize=(8, 4))
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=.08, hspace=.5)

    for i in range(6):
        id = ids.pop()

        preds = fill_regressor(str(id))
        ax0 = f.add_subplot(321 + i)
        tmp = rand_history(id=str(id), hours=500)
        ax0.plot(range(len(tmp)), tmp, label="sim " + str(id + 1))

        for d, n in zip(tmp, range(len(tmp))):
            if d == 0:
                ax0.plot([n, n + 100], [0, 100*preds], 'r')

        ax0.set_xlim(0, len(tmp))
        ax0.set_ylim(0, 101)
        ax0.set_xlabel("Time (h)")
        ax0.set_ylabel("Fill Level (%)")
        ax0.set_title("Showing simulation for sensor {0}".format(id))

    plt.show()