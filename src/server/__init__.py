from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Globally accessible libraries
db = SQLAlchemy()


def init_app():
    """Initialize the core application."""
    app = Flask(__name__, instance_relative_config=False)
    # app.config.from_object('config.Config')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
    app.config['SECRET_KEY'] = 'dev'  # Secret key so we can use sessions

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Include our Routes
        from .apps import routes
        from .bins import routes
        from .trucks import routes
        from .users import routes
        from . import auth  # Temp (auth/register, auth/login, auth/logout)
        from . import views  # Temp ('index')

        # Register Blueprints
        app.register_blueprint(bins.routes.bins_blueprint)
        app.register_blueprint(apps.routes.apps_blueprint)
        app.register_blueprint(trucks.routes.trucks_blueprint)
        app.register_blueprint(users.routes.users_blueprint)
        app.register_blueprint(auth.auth_blueprint)  # Temp
        app.register_blueprint(views.bp)  # Temp

        # Create sql tables from data models
        print("Creating SQL Tables")
        db.create_all()

        '''Start of Flask-Login configuration'''

        from .models import User

        # Create login manager
        login_manager = LoginManager()
        # Customize the login process
        login_manager.login_view = "auth_blueprint.login"
        login_manager.login_message = ['Please log in to access this page.']
        login_manager.login_message_category = 'warning'
        # Configure login manager
        login_manager.init_app(app)

        # Callback to reload the user object from the user ID stored in the session
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(user_id)

        '''End of Flask-Login configuration'''

        return app
