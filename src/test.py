# This is the code
# Find me on discord ZDev1#4511
# We shouldn't install flask in the terminal, it is already imported

from flask import Flask
from apps.routes import apps_blueprint
from bins.routes import bins_blueprint
from trucks.routes import trucks_blueprint

app = Flask(__name__)
app.debug = True

# Register the blueprints
# app.register_blueprint(apps_blueprint)
app.register_blueprint(bins_blueprint)
# app.register_blueprint(trucks_blueprint)


@app.route('/', methods=['GET'])
def test():
    return 'Hello world'
    pass


if __name__ == "__main__":
    app.run(port=3000, debug=True)
    # if you need to make it live debuging add 'debug=True'
    # app.run(port=3000, debug=True)

   # Hope you enjoyed ;)
