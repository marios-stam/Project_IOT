from flask import Blueprint

apps_blueprint = Blueprint('apps_blueprint', __name__)


@apps_blueprint.route('/app', methods=['POST'])  # create new truck
def create_app():
    print("Create new truck")
    pass


# update a truck
@apps_blueprint.route('/app/<truck_id>', methods=['PUT'])
def parse_app(truck_id=None):
    print("Parsing new Bin with id:", truck_id)  # parse truck
    pass
