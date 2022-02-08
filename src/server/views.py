from flask import Blueprint, jsonify, render_template

bp = Blueprint('views', __name__)


@bp.route('/')
def index():
    # data = [{
    #     "type": "Feature",
    #     "properties": {
    #         "id": 32,
    #         "status": "status",
    #         "updated": "updated",
    #         "fullness": 66,
    #     },
    #     "geometry": {
    #         "type": "Point",
    #         "coordinates": [23.833873, 38.019308],
    #     }
    # }, {
    #     "type": "Feature",
    #     "properties": {
    #         "id": 68984,
    #         "status": "asfdapskodf",
    #         "updated": ".............",
    #         "fullness": 89,
    #     },
    #     "geometry": {
    #         "type": "Point",
    #         "coordinates": [23.833787, 38.01542],
    #     }
    # }]
    # return jsonify(data)
    return render_template("index.html")
