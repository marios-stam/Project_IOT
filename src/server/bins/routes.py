from flask import Blueprint, make_response
from flask import current_app as app
from ..models import db, Bin
from datetime import datetime as dt

bins_blueprint = Blueprint('bins_blueprint', __name__)


@bins_blueprint.route('/test')
def tested():
    return "Tested"


@bins_blueprint.route('/bins')  # create new bin
def create_bin():
    result = db.session.query(Bin).filter(Bin.id == 0).all()
    if(len(result) == 0):
        print("Create new bin")

        new_bin = Bin(
            id=0,
            status=100,
            fullness=50,
            updated=dt.now(),
            position="x: 5, y: 5"
        )

        db.session.add(new_bin)  # Adds new User record to database

    else:
        result[0].fullness = 22
        result[0].updated = dt.now()
        new_bin = result[0]

    db.session.commit()  # Commits all changes
    return make_response(f"{new_bin} successfully created/updated!")


@bins_blueprint.route('/bins/<bin_id>', methods=['POST'])  # update a bin
def parse_bin(bin_id=None):
    print("Parsing new Bin")  # parse bin
    pass
