# backend/tests/conftest.py

import pytest
from app import create_app
from database import Base, engine
# 重要：必須引入 models，這樣 Base 才知道有哪些表要建立
from models import User 

@pytest.fixture
def client():
    # 1. 建立 App
    app = create_app()
    app.config['TESTING'] = True

    # 2. 建立所有資料表 (搬家具進去)
    with app.app_context():
        Base.metadata.create_all(bind=engine)

    # 3. 提供測試用的 client 給測試程式使用
    with app.test_client() as client:
        yield client

    # 4. 測試結束後清理 (拆家具)
    with app.app_context():
        Base.metadata.drop_all(bind=engine)