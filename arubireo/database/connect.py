from sqlalchemy.orm import Session, sessionmaker

from arubireo.database.models import Bill, User


class Connection:
    def __init__(self, engine) -> None:
        self._session = sessionmaker(bind=engine)()

    def create_user(self, user_id: str) -> None:
        user = User(user_id=user_id)
        self._session.add(user)
        self._session.commit()

    def add_bill(self, user_id: str, description: str, amount: str) -> None:
        bill = Bill(user_id=user_id, description=description, amount=amount)
        self._session.add(bill)
        self._session.commit()

    def get_date(self, user_id: str, date) -> list:
        res = (
            self._session.query(Bill)
            .filter_by(user_id=user_id, date=date)
            .all()
        )
        return res

    def get_dates(self, user_id: str, start: str, end: str) -> list:
        print(start, end)
        res = (
            self._session.query(Bill)
            .filter_by(user_id=user_id)
            .filter(Bill.date >= start, Bill.date <= end)
            .all()
        )
        return res

    @property
    def session(self) -> Session:
        return self._session
