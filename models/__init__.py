from sqlalchemy import create_engine

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
import config
from config import CURRENT_ENV

engine = create_engine(config.as_dict()[CURRENT_ENV].SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from models.models import Product

    Base.metadata.create_all(bind=engine)
