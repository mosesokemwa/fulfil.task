from flask import Flask
from api import api
import config
from models import db_session, init_db


def create_app():
    app = Flask(__name__)
    # logger.info(f'Starting app in {config.APP_ENV} environment')
    app.config.from_object(config)
    api.init_app(app)

    init_db()
    # testing db connections
    # query_rows = db_session.execute("SELECT * FROM product").fetchall()
    # for register in query_rows:
    #     print(f"{register.col_1_name}, {register.col_2_name}, ..., {register.col_n_name}")

    # from app.upload import bp as upload_bp

    # app.register_blueprint(upload_bp, url_prefix="/upload")

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db_session.remove()

    # if not app.debug and not app.testing:
    # ... no changes to logging setup

    return app

# if __name__ == "__main__":
#    app = create_app()
#    app.run(host='0.0.0.0', debug=True)
