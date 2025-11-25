# backend/models.py
from sqlalchemy import Column, Integer, String, Boolean, Index
from database import Base  # 从 database.py 导入 Base, 擇一，建議用絕對路徑

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    # email = Column(String, unique=True, nullable=False, index=True)  # 添加索引
    email = Column(String, unique=True, nullable=False)  # 添加索引

    password = Column(String, nullable=False)
    address = Column(String, nullable=False)
    is_driver = Column(Boolean, default=False, nullable=False)
    is_participating = Column(Boolean, default=True, nullable=False)

    # 已經對 email 設了 unique=True，PostgreSQL 會自動建立唯一索引；再加 Index('ix_email', 'email') 會重複，建議移除 __table_args__ 這段與 index=True

    # 添加索引到表
    # __table_args__ = (
    #     Index('ix_email', 'email'),  # 確保索引存在
    # )
