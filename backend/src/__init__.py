import json
import logging

from flask import Flask
from src.configs.logging_configs import initialize_logging_configs

from src.extensions.extensions import db, jwt, bcrypt, cors

from src.routes.app_routes import users_blueprint

from src.configs.initial_data import initialize_database

if __name__ == "__main__":
    """
    initializing the logger before creating flask app
    to use logging library instead of app.logger
    """
    initialize_logging_configs()

    logger = logging.getLogger(__name__)
    logger.info("initializing flask application")

    app = Flask(__name__)
    app.config.from_file("configs\\app-configs.json", load=json.load)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(users_blueprint)

    with app.app_context():
        initialize_database()

    with open("configs\\app-configs.json", "r") as props_file:
        app.run(debug=True, port=json.load(props_file)["APP_PORT"])