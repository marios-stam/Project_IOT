from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Globally accessible libraries
db = SQLAlchemy()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from .apps import routes
        from .bins import routes
        from .trucks import routes

        # Register Blueprints
        app.register_blueprint(bins.routes.bins_blueprint)
        app.register_blueprint(apps.routes.apps_blueprint)
        app.register_blueprint(trucks.routes.trucks_blueprint)

        # Create sql tables from data models
        print("Creating SQL Tables")
        db.create_all()

        return app
