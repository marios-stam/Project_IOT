import json

from flask import Blueprint, abort, jsonify, render_template, request
from flask_login import current_user, login_required

from .. import db
from ..models import Bin, Truck, User

client_blueprint = Blueprint(
    'client_blueprint', __name__, url_prefix='/client')


@client_blueprint.route('/citizen')
@login_required
def citizen():
    if User.query.get(current_user.id).role != 'citizen':
        abort(403)
    return render_template('client/citizen.html')


@client_blueprint.route('/citizen/charge')
def charge_sensor():
    bin_id = request.args.get('bin_id', type=int)
    bin = Bin.query.get(bin_id)
    bin.battery = bin.battery + 2
    db.session.commit()
    return json.dumps({'success': True}), 200


@client_blueprint.route('/driver')
@login_required
def driver():
    if User.query.get(current_user.id).role != 'driver':
        abort(403)
    return render_template('client/driver.html')


@client_blueprint.route('/driver/routing')
def driver_routing():
    available_trucks = Truck.query.filter_by(status=0).all()
    trucks_arr = []
    for truck in available_trucks:
        trucks_arr.append((truck.id, truck.long, truck.lat))
    print(trucks_arr)

    bins_to_collect = Bin.query.filter(Bin.fill_level > 80).all()
    bins_arr = []
    for bin in bins_to_collect:
        bins_arr.append((bin.long, bin.lat))
    print(bins_arr)

    # shit happens here

    result = [
        {
            "truck_id": 1,
            "route_coords": [
                [9.997521, 53.551168],
                [9.998489, 53.551736],
                [9.997942, 53.552081],
                [9.998752, 53.55251],
                [9.999358, 53.552127],
                [9.999091, 53.551991],
                [9.999358, 53.552127],
                [9.998752, 53.55251],
                [9.999705, 53.553024],
                [9.998942, 53.553462],
                [9.998112, 53.552937]
            ]
        },
        {
            "truck_id": 2,
            "route_coords": [
                [11.56971, 48.143908],
                [11.569473, 48.144239],
                [11.56949, 48.144403],
                [11.569697, 48.144653],
                [11.569571, 48.144918],
                [11.569954, 48.145094],
                [11.570344, 48.145179],
                [11.570722, 48.145134],
                [11.570716, 48.145297],
                [11.569762, 48.145614],
                [11.569454, 48.145133],
                [11.56917, 48.145043],
                [11.568859, 48.144982],
                [11.568668, 48.144826],
                [11.568642, 48.144597],
                [11.568861, 48.144236],
                [11.567883, 48.142686],
                [11.559557, 48.145122],
                [11.559342, 48.145922]
            ]
        }
    ]

    for r in result:
        if r['truck_id'] == request.args.get('truck_id', type=int):
            return r


@client_blueprint.route('/driver/route')
def get_route():
    truck_id = request.args.get('truck_id', type=int)
    return jsonify(truck_id)


@client_blueprint.route('/driver/empty')
def empty_bin():
    pass


@client_blueprint.route('/mngr')
@login_required
def mngr():
    if User.query.get(current_user.id).role != 'mngr':
        abort(403)
    return render_template('client/mngr.html')
