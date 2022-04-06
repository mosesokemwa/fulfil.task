from flask import Flask
from config import Config
from .database import db_session, init_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_db()
    # testing db connections
    # query_rows = db_session.execute("SELECT * FROM product").fetchall()
    # for register in query_rows:
    #     print(f"{register.col_1_name}, {register.col_2_name}, ..., {register.col_n_name}")

    from app.upload import bp as upload_bp

    app.register_blueprint(upload_bp, url_prefix="/upload")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # if not app.debug and not app.testing:
    # ... no changes to logging setup

    return app


from app import models
