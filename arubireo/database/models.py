from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.types import Date, Time

Base = declarative_base()


class User(Base):
    __tablename__: str = "user"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, nullable=False)
    bill = relationship("Bill")

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id})"


class Bill(Base):
    __tablename__: str = "bill"

    id = Column(Integer, primary_key=True)
    user_id = Column(String, ForeignKey("user.user_id"), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    date = Column(Date, nullable=False, default=datetime.utcnow().date)
    time = Column(Time, nullable=False, default=datetime.utcnow().time)

    def __repr__(self) -> str:
        return (
            f"Bill(user_id={self.user_id}, description={self.description},"
            f"amount={self.amount}, date={self.date}, time={self.time})"
        )
