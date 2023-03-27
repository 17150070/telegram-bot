from typing import Optional

from sqlalchemy import text, Row

from database import db_session, engine
from models.users import User


def create_user_by_telegram_id(telegram_id: int) -> None:
    with engine.connect() as connection:
        insert_user_query = text("INSERT INTO telegram_users (telegram_id, balance, is_admin) VALUES (:telegram_id, 0, false)")
        connection.execute(insert_user_query, {"telegram_id": telegram_id})
        connection.commit()

    # with db_session() as session:
    #     session.

def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    with engine.connect() as connection:
        insert_user_query = text("SELECT id, balance, is_admin FROM telegram_users WHERE telegram_id = :telegram_id LIMIT 1")
        cursor = connection.execute(insert_user_query, {"telegram_id": telegram_id})
        result: Row = cursor.fetchone()
        if result is None:
            return None
        return User(id=result[0], telegram_id=telegram_id, balance=result[1], is_admin=result[2])

