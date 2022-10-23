from sqlalchemy import create_engine

from arubireo import env
from arubireo.database.connect import Connection
from arubireo.database.models import Base

engine = create_engine(env.sqlalchemy_database_url)


Base.metadata.create_all(engine)


connection = Connection(engine)
