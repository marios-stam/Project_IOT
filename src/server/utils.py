from matplotlib import pyplot as plt
import numpy as np
import json
from datetime import datetime
from random import randint


def diff_time(t1, t2) -> int:
    if type(t1) is str:
        try:
            t1 = datetime.strptime(t1, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            try:
                t1 = datetime.strptime(t1[:-4], '%d-%m-%Y %H:%M:%S')
            except ValueError:
                t1 = datetime.strptime(t1[:-4], '%a, %d %b %Y %H:%M:%S')
    if type(t1) is str:
        try:
            t2 = datetime.strptime(t2, '%d/%m/%Y %H:%M:%S')
        except ValueError:
            try:
                t2 = datetime.strptime(t2[:-4], '%d-%m-%Y %H:%M:%S')
            except ValueError:
                t2 = datetime.strptime(t2[:-4], '%a, %d %b %Y %H:%M:%S')

    res = t2 - t1
    if res.days < 0:
        raise Exception("Cannot process measurement from the future!")

    return int(res.total_seconds())


def rand_perc(inc: bool = False, neg: bool = False, center: bool = False) -> float:
    res = randint(0, 10000000) / 10000000
    if inc:
        return res + 1
    if neg:
        return res * -1
    if center:
        return (res - 0.5) * 2
    return res


def is_perc(perc: float) -> bool:
    return 0 <= perc <= 1


def rand_check(chance: float) -> bool:
    perc = rand_perc()
    if not is_perc(perc) or not is_perc(chance):
        raise Exception("Number is not percentage")
    return perc > (1 - chance)


class AccelData:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, p):
        self.x += p.x
        self.y += p.y
        self.z += p.z

    def __sub__(self, p):
        self.x -= p.x
        self.y -= p.y
        self.z -= p.z

    def __mul__(self, k: float):
        self.x *= k
        self.y *= k
        self.z *= k

    def __iter__(self):
        yield 'x', self.x
        yield 'y', self.y
        yield 'z', self.z

# === MOCK DATA ===
def rand_history_to_full():
    base_rate = 2.5 + (1 * rand_perc(center=True))
    res = [0]
    while res[-1] <= 100:
        res.append(res[-1] + base_rate * max(0, (0.5 + 0.75*rand_perc(center=True))))
    del res[-1]
    return np.array(res)


def rand_history(id, hours=168):
    # Try to get data from file
    try:
        with open('./bin/dummy_rates.json', 'r', encoding='utf-8') as f:
            base_rates = json.load(f)
    # Create file if missing
    except FileNotFoundError:
        with open('./bin/dummy_rates.json', 'w', encoding='utf-8') as f:
            json.dump({}, f, indent=4)

        return rand_history(id, hours)

    # Generate base rate for new IDs
    if id not in base_rates:
        base_rates[id] = 2.5 + (1 * rand_perc(center=True))

        with open('./bin/dummy_rates.json', 'w', encoding='utf-8') as f:
            json.dump(base_rates, f, indent=4)

    res = [0]

    # Generate data
    for i in range(hours):
        res.append(min(100, res[-1] + base_rates[id] * max(0, (0.5 + 0.75 * rand_perc(center=True)))))
        if rand_check(rand_perc() * 0.05 * res[-1] / 100):
            res[-1] = 0

    return np.array(res)


# === DEBUG ===
def graph_rand_to_full_history(rep=100, sensor_id=None):
    mx = -float('inf')
    lens = []

    f, (ax0, ax1) = plt.subplots(1, 2, gridspec_kw={'width_ratios': [2, 1]}, figsize=(12, 5))
    plt.tight_layout(2)

    for i in range(rep):
        tmp = rand_history_to_full()

        r = hex(int(min(1, max(0, (len(tmp) - 30)/130)) * 255)).strip('0x')
        col = ("#" + r.rjust(2, '0') + '0000').upper()
        lens.append(len(tmp))

        if i % 10 == 0:
            ax0.plot(range(len(tmp)), tmp, color=col, label="sim " + str(i+1))
            if len(tmp) > mx: mx = len(tmp)
    ax0.set_xlim(0, mx)
    ax0.set_ylim(0, 101)
    ax0.set_xlabel("Time (h)")
    ax0.set_ylabel("Fill Level (%)")
    ax0.set_title("Showing {0} of {1} simulations".format(rep//10, rep))

    ax1.hist(lens, bins=20)
    ax1.set_title("Distribution: ??=" + str(np.mean(lens)) + ", ??=" + '{0:.2f}'.format(np.std(lens)))
    ax1.set_xlabel("Time (h)")

    plt.show()


def graph_rand_history(rep=10):
    tmp = None

    f = plt.figure(figsize=(8, 4))
    ax0 = f.add_subplot(111)

    for i in range(rep):
        tmp = rand_history(id=str(i))
        ax0.plot(range(len(tmp)), tmp, label="sim " + str(i+1))

    ax0.set_xlim(0, len(tmp))
    ax0.set_ylim(0, 101)
    ax0.set_xlabel("Time (h)")
    ax0.set_ylabel("Fill Level (%)")
    ax0.set_title("Showing {0} simulations".format(rep))

    plt.show()
