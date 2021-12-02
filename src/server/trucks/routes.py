from flask import Blueprint

trucks_blueprint = Blueprint('trucks_blueprint', __name__)


@trucks_blueprint.route('/trucks', methods=['POST'])  # create new truck
def create_truck():
    print("Create new truck")
    pass


# update a truck
@trucks_blueprint.route('/trucks/<truck_id>', methods=['PUT'])
def parse_truck(truck_id=None):
    print("Parsing new truck with id:", truck_id)  # parse truck
    pass
