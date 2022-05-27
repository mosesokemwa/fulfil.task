from flask import Flask
from api import api
import config
from models import db_session, init_db
import logging
import os

logging.basicConfig(
    level=logging.DEBUG,
    format=f"[%(asctime)s]: {os.getpid()} %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger()


def create_app():
    app = Flask(__name__)
    logger.info(f"Starting app in {config.APP_ENV} environment")
    # logger.info(f'Starting app in {config.APP_ENV} environment')
    app.config.from_object(config)
    api.init_app(app)

    init_db()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    return app


if __name__ == "__main__":
   app = create_app()
   app.run(host='0.0.0.0', debug=True)
