from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import timedelta
from flask_login import LoginManager
from flask_migrate import Migrate

# alchemy instance
db = SQLAlchemy()

# login mana. instance
login_manager = LoginManager()


# migrate instance. instance for db migrations
migrate = Migrate()

# func. to create app
def create_app():
    # init. the app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = "whatever we wanna trigger as our secret key"
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=30)

    # init. database
    db.init_app(app)

    # init. migrate
    migrate.init_app(app, db)

    # init. login manager
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    login_manager.login_message_category = 'info'

    # user loader for the login manager
    @login_manager.user_loader
    def user_loader(user_id):
        from app.models import User
        return User.query.get(user_id)


    # registering routes/endpoints of the app
    from app.admin import admin
    from app.auth import auth
    from app.views import view
    app.register_blueprint(admin)
    app.register_blueprint(auth)
    app.register_blueprint(view)
    return app
