import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# 建議加上 pool_pre_ping 與 future 以提升穩定度與 2.0 相容性
engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, future=True)
Base = declarative_base()

def init_db():
    # 用絕對匯入，確保 Alembic 也找得到
    from backend import models
    Base.metadata.create_all(bind=engine)
    print("Database initialized!")