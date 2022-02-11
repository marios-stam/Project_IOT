from flask import request, make_response
from ..models import Bin, db, Bounty, User
from flask import jsonify
from datetime import datetime as dt
from ..utils import diff_time
from ..__config__ import BOUNTY_DEADLINE
import geopy.distance
from datetime import datetime
from copy import deepcopy
import requests


def get_bounty(bounty_id=None):
    result = db.session.query(Bounty).filter(Bounty.id == bounty_id).all()
    if(len(result) == 0):
        return make_response(f"No bounty found with ID: {bounty_id}")
    else:
        print(f"Gettind data of bounty: {bounty_id} ...")
        data = result[0].__dict__
        
        if check_unassign_usr(data):
            return get_bounty(bounty_id)

        data.pop('_sa_instance_state')
        data_json = jsonify(data)
        return make_response(data_json)


def update_bounty(data=None):
    if data is None:
        data = request.get_json()

    id = data['id']
    result = db.session.query(Bounty).filter(Bounty.id == id).all()
    if(len(result) == 0):
        return create_bounty(data)

    print(f"Updating bounty with ID:{id} ...")
    for key, value in data.items():
        if key == 'created' or key == 'updated':
            result[0].updated = dt.now()
            continue

        setattr(result[0], key, value)

    db.session.commit()

    return make_response(f"Updated bounty with ID:{id}")


def create_bounty(data=None):
    if data == None:
        data = request.get_json()

    data['timestamp'] = dt.now()  # set created date
    # data['time_assigned'] = dt.now()  # set created date

    new_bounty = Bounty(**data)

    # add to database
    db.session.add(new_bounty)
    db.session.commit()
    return make_response(f"New bounty created with ID:{new_bounty.id}")


def get_all_bounties():
    print("Getting all Bounties")

    result = db.session.query(Bounty).all()
    if(len(result) == 0):
        return make_response(f"No bounty found!")

    bounties = []
    refresh = []
    for i in range(len(result)):
        bounty = result[i].__dict__
        
        bounty_json = {
            'id': bounty['id'],
            'timestamp': bounty['timestamp'],
            'bin_id': bounty['bin_id'],
            'message': bounty['message'],
            'points': bounty['points'],
            'type': bounty['type'],
            'assigned_usr_id': bounty['assigned_usr_id'],
            'time_assigned': bounty['time_assigned'],
            'completed': bounty['completed'],
        }

        if bounty['assigned_usr_id'] is not None and diff_time(bounty['time_assigned'], datetime.now()) > BOUNTY_DEADLINE and not bounty['completed']:
            refresh.append(bounty['id'])
            bounty_json['assigned_usr_id'] = None
            bounty_json['time_assigned'] = None
        
        # I had to make it work ffs
        bounties.append(bounty_json)

    for id_ in refresh:
        # print(f"Unissigning user {bounty['assigned_usr_id']} from bounty {bounty['id']}! Time limit exceeded.")
        update_bounty({
            'id': id_,
            'time_assigned': None,
            'assigned_usr_id': None
        })

    return jsonify(bounties)


def get_uncompleted_bounties_in_radius():
    # Getting all bounties within radius
    # pos--> (long, lat)
    # radius--> in km

    # get data from json
    data = request.get_json()
    pos = (data['long'], data['lat'])
    radius = float(data['radius'])

    result = db.session.query(Bounty).filter(Bounty.completed == False).all()

    if(len(result) == 0):
        return make_response(f"No bounty found!")
    else:
        result = [{
                'id': bounty.__dict__['id'],
                'long': bounty.__dict__['long'],
                'lat': bounty.__dict__['lat'],
                'timestamp': bounty.__dict__['timestamp'],
                'bin_id': bounty.__dict__['bin_id'],
                'message': bounty.__dict__['message'],
                'points': bounty.__dict__['points'],
                'type': bounty.__dict__['type'],
                'assigned_usr_id': bounty.__dict__['assigned_usr_id'],
                'time_assigned': bounty.__dict__['time_assigned'],
                'completed': False
            } for bounty in result]

    bounties = []
    refresh = []
    flag = False
    for bounty in result:
        distance = geopy.distance.distance(pos, (bounty['long'], bounty['lat'])).km

        if bounty['assigned_usr_id'] is not None and diff_time(bounty['time_assigned'], datetime.now()) > BOUNTY_DEADLINE and not bounty['completed']:
            refresh.append(bounty['id'])
            flag = True

        if distance <= radius:
            bounty['assigned_usr_id'] = None if flag else bounty['assigned_usr_id']
            bounty['time_assigned'] = None if flag else bounty['time_assigned']
            bounties.append(bounty)

        flag = False

    for id_ in refresh:
        # print(f"Unissigning user {bounty['assigned_usr_id']} from bounty {bounty['id']}! Time limit exceeded.")
        update_bounty({
            'id': id_,
            'time_assigned': None,
            'assigned_usr_id': None
        })

    return jsonify(bounties)


def assign_bounty(bounty_id, usr_id):
    result = get_bounty(bounty_id).json
    if len(result) == 0:
        return make_response(f"Bounty with id {bounty_id} not found!", 404)
    if result['assigned_usr_id'] is not None and not check_unassign_usr(result):
        return make_response(f"Bounty with id {bounty_id} is already assigned to a user!", 403)

    update_bounty({
        'id': bounty_id,
        'time_assigned': datetime.now(),
        'assigned_usr_id': usr_id
    })

    return make_response(f"Succesfully assigned {usr_id} to bounty {bounty_id}")


def complete_bounty(bounty_id, usr_id):

    # Checks for Bounty row
    bounty = get_bounty(bounty_id).json
    points = deepcopy(bounty['points'])
    type = deepcopy(bounty['type'])
    sensor_id = deepcopy(bounty['bin_id'])
    if len(bounty) == 0:
        return make_response(f"Bounty with id {bounty_id} not found!", 404)
    if bounty['assigned_usr_id'] != usr_id:
        return make_response(f"The user with id {usr_id} is not assigned to this bounty!", 403)
    if bounty['completed']:
        return make_response(f"The bounty with id {bounty_id} is already completed!", 403)

    # Checks for User row
    usr = db.session.query(User).filter(User.id == usr_id).all()
    if len(usr) == 0:
        return make_response(f"User with id {usr_id} not found!", 404)
    elif len(usr) > 1:
        return make_response(f"Multiple users with id {usr_id} were found!", 500)
    
    if type == 'fire':
        requests.post("http://localhost:26223/send_msg/" + sensor_id + '/off_fire')
    elif type == 'fall':
        requests.post("http://localhost:26223/send_msg/" + sensor_id + '/off_fall')
    elif type == 'battery':
        requests.post("http://localhost:26223/send_msg/" + sensor_id + '/charge')
    else:
        return make_response("Unknown bounty type", 403)

    # Update bounty
    update_bounty({
        'id': bounty_id,
        'completed': True
    })
    
    # Update user
    setattr(usr[0], 'points', int(usr[0].points) + int(points))
    db.session.commit()

    return make_response(f"Succesfully closed bounty {bounty_id} and awarded {usr_id} with {bounty['points']} points")


def get_uncompleted_bounties_of_user(usr_id):
    result = db.session.query(Bounty).filter(
        Bounty.assigned_usr_id == usr_id).filter(Bounty.completed == False).all()

    if(len(result) == 0):
        return make_response(f"No uncompleted bounty found for user with user_id:", usr_id, "!")

    bounties = []
    refresh = []
    for i in range(len(result)):
        bounty = result[i].__dict__

        if bounty['assigned_usr_id'] is not None and diff_time(bounty['time_assigned'], datetime.now()) > BOUNTY_DEADLINE and not bounty['completed']:
            refresh.append(bounty['id'])
        else:
            bounty_json = {
                'id': bounty['id'],
                'timestamp': bounty['timestamp'],
                'bin_id': bounty['bin_id'],
                'message': bounty['message'],
                'points': bounty['points'],
                'type': bounty['type'],
                'assigned_usr_id': bounty['assigned_usr_id'],
                'time_assigned': bounty['time_assigned'],
                'completed': bounty['completed'],
            }

            bounties.append(bounty_json)

    for id_ in refresh:
        # print(f"Unissigning user {bounty['assigned_usr_id']} from bounty {bounty['id']}! Time limit exceeded.")
        update_bounty({
            'id': id_,
            'time_assigned': None,
            'assigned_usr_id': None
        })

    return jsonify(bounties)


def check_unassign_usr(bounty):
    if bounty['assigned_usr_id'] is None:
        return False

    elif diff_time(bounty['time_assigned'], datetime.now()) > BOUNTY_DEADLINE and not bounty['completed']:
        print(f"Unissigning user {bounty['assigned_usr_id']} from bounty {bounty['id']}! Time limit exceeded.")
        update_bounty({
            'id': bounty['id'],
            'time_assigned': None,
            'assigned_usr_id': None
        })
        return True

    return False