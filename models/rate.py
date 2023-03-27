from sqlalchemy import Column, Integer, String

from database import Base


class Rate(Base):
    __tablename__ = 'telegram_rate'
    id = Column(Integer, primary_key=True)
    rate = Column(String)
    user_id = Column(Integer, nullable=True)
