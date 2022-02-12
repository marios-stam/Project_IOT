import json, os

with open(os.path.join(os.getcwd(), 'server/constants.json')) as f:
    consts = json.load(f)