import random
import secrets
from datetime import datetime, timedelta

import pytest

from arubireo.database.connect import Connection
from arubireo.database.models import Bill, User


def test_insert(dbsession):
    user = User(user_id="abc")
    assert str(user) == "User(user_id=abc)"
    dbsession.add(user)
    assert dbsession.query(User).first() == user
    bill = Bill(user_id="abc", description="eat", amount=50)
    dbsession.add(bill)
    db_bill = dbsession.query(Bill).first()
    assert db_bill.user_id == "abc"
    assert db_bill.description == "eat"
    assert db_bill.amount == 50


class TestConnect:
    @pytest.fixture(scope="class")
    def connection(self, engine):
        return Connection(engine)

    @pytest.fixture(scope="class")
    def user_id(self):
        return secrets.token_hex(8)

    @pytest.fixture(scope="class", autouse=True)
    def bill_args(self, user_id):
        return {
            "user_id": user_id,
            "description": "eat",
            "amount": random.randint(1, 1000),
        }

    @pytest.fixture(scope="class")
    def bill(self, bill_args):
        bill = Bill(**bill_args)
        return bill

    def test_create_user(self, connection, dbsession, user_id):
        connection.create_user(user_id=user_id)
        db_user = dbsession.query(User).first()
        assert db_user.user_id == user_id

    def test_add_bill(self, connection, dbsession, bill_args, bill):
        connection.add_bill(**bill_args)
        db_bill = dbsession.query(Bill).first()
        assert db_bill.user_id == bill.user_id
        assert db_bill.description == bill.description
        assert db_bill.amount == bill.amount

    def test_get_date(self, connection, bill):
        date = datetime.utcnow().date() - timedelta(days=2)
        assert not connection.get_date(user_id=bill.user_id, date=date)
        assert connection.get_date(
            user_id=bill.user_id, date=datetime.utcnow().date()
        )
        start = datetime.utcnow().date() - timedelta(days=2)
        end = datetime.utcnow().date() + timedelta(days=1)
        assert connection.get_dates(user_id=bill.user_id, start=start, end=end)
        start = datetime.utcnow().date() + timedelta(days=2)
        end = datetime.utcnow().date() + timedelta(days=4)
        assert not connection.get_dates(
            user_id=bill.user_id, start=start, end=end
        )
