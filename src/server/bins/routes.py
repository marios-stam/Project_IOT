from flask import Blueprint
from flask import current_app as app

bins_blueprint = Blueprint('bins_blueprint', __name__)


@bins_blueprint.route('/test')
def tested():
    return "Tested"


@bins_blueprint.route('/bins', methods=['POST'])  # create new bin
def create_bin():
    print("Create new bin")
    pass


@bins_blueprint.route('/bins/<bin_id>', methods=['POST'])  # update a bin
def parse_bin(bin_id=None):
    print("Parsing new Bin")  # parse bin
    pass
