from sqlalchemy import Column, Integer, Boolean, BigInteger

from database import Base


class User(Base):
    __tablename__ = 'telegram_users'
    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True)
    balance = Column(Integer)
    is_admin = Column(Boolean)
