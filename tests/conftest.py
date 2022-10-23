import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from arubireo.database.models import Base


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///tests/sql_test.db")


@pytest.fixture(scope="class")
def tables(engine):
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(scope="class")
def dbsession(engine, tables):
    connection = engine.connect()

    session = Session(bind=connection)

    yield session

    session.close()

    connection.close()
