from datetime import datetime

from sqlalchemy import TIMESTAMP, Column, ForeignKey, Integer, String

from src.database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, nullable=False, unique=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)


class SubscriptionType(Base):
    __tablename__ = "subscription_type"

    type_id = Column(Integer, primary_key=True)
    type_name = Column(String, unique=True, nullable=False)
    monthly_price = Column(Integer, nullable=False)


class UserSubscription(Base):
    __tablename__ = "user_subscription"

    subscription_id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey("user.telegram_id"))
    type_id = Column(Integer, ForeignKey("subscription_type.type_id"))
    valid_from = Column(TIMESTAMP, nullable=False)
    valid_to = Column(TIMESTAMP, nullable=False)


class Action(Base):
    __tablename__ = "action"

    action_id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, ForeignKey("user.telegram_id"))
    response_id = Column(Integer, nullable=True)
    platform_type = Column(String, nullable=True)
    resource_name = Column(String, nullable=True)
    query = Column(String, nullable=True)
    prompt = Column(String, nullable=True)
    response = Column(String, nullable=True)
    input_tokens = Column(Integer, nullable=True)
    output_tokens = Column(Integer, nullable=True)
    execution_time = Column(Integer, nullable=True)
    feedback = Column(String, nullable=True)

class ChannelsPool(Base):
    __tablename__ = "channels_pool"
    channel = Column(String, primary_key=True)
    user_id = Column(Integer, nullable=True)
    username= Column(String, nullable=True)
    added_date = Column(TIMESTAMP, default=datetime.utcnow)
    members_count = Column(Integer, nullable=True)