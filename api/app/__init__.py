from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config
import os

db = SQLAlchemy()
migrate = Migrate()

# create a flask app
def create_app(config_class=Config):
    app = Flask("trvl")

    app.config.from_object(config_class)
    db.init_app(app)

    # import blueprint
    from app.routes import api_bp
    app.register_blueprint(api_bp)

    # migrate db
    migrate.init_app(app, db)

    # init migrations directory if it doesn't exist
    migrations_dir = os.path.join(app.root_path, 'migrations')
    if not os.path.exists(migrations_dir):
        with app.app_context():
            from flask_migrate import init
            init(directory='migrations')

    # create db tables
    with app.app_context():
        db.create_all()

    return app