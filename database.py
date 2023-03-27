from sqlalchemy import create_engine
from sqlalchemy.ext.compiler import compiles
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql.ddl import CreateColumn

SQLALCHEMY_DATABASE_URL = "postgresql://telegram_bot_user:telegram_bot_pass@localhost:5433/telegram_bot_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

db_session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
