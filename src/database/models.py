from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String

from src.database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)


class SubscriptionType(Base):
    __tablename__ = "subscription_type"

    type_id = Column(Integer, primary_key=True)
    type_name = Column(String, unique=True, nullable=False)
    monthly_price = Column(Integer, nullable=False)


class UserSubscription(Base):
    __tablename__ = "user_subscription"

    subscription_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id"))
    type_id = Column(Integer, ForeignKey("subscription_type.type_id"))
    valid_from = Column(TIMESTAMP, nullable=False)
    valid_to = Column(TIMESTAMP, nullable=False)
