from sqlalchemy import Column, ForeignKey, Integer, create_engine, String

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship, scoped_session, sessionmaker
from config import Config

# engine = create_engine('postgresql://mosesokemwa:password@localhost:5432/fulfil')
# engine = create_engine('postgresql+psycopg2://mosesokemwa:password@localhost:5432/fulfil?port=5432')
engine = create_engine(Config.SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))


Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    from app.models import Product
    Base.metadata.create_all(bind=engine)