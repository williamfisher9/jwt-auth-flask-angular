import json
import logging

from flask import Flask
from src.configs.logging_configs import initialize_logging_configs

from src.extensions.extensions import db, jwt, bcrypt

if __name__ == "__main__":
    initialize_logging_configs()

    logger = logging.getLogger(__name__)
    logger.info("initializing flask application")

    app = Flask(__name__)
    app.config.from_file("configs\\app-configs.json", load=json.load)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    app.run(debug=True)