from matplotlib import pyplot as plt
import numpy as np
import json
from datetime import datetime
from random import randint


def diff_time(t1, t2) -> int:
    if type(t1) is str:
        t1 = datetime.strptime(t1, '%d/%m/%Y %H:%M:%S')
    if type(t1) is str:
        t2 = datetime.strptime(t2, '%d/%m/%Y %H:%M:%S')

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
