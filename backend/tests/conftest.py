# backend/tests/conftest.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
# 注意：這裡改成 import 整個 database 模組，而不是只 import engine
# 這樣我們才能在下面動態替換掉它，而不會動到真的資料庫
import database 
from app import create_app
from models import User 

@pytest.fixture
def client():
    # 1.設定測試用的「記憶體資料庫」
    # "sqlite:///:memory:" 表示資料只存在 RAM 裡，程式一關就消失，絕對不會碰到硬碟
    # check_same_thread=False 是 SQLite 在 Flask 測試時的特殊設定，防止線程錯誤
    test_engine = create_engine(
        "sqlite:///:memory:", 
        connect_args={"check_same_thread": False},
        pool_pre_ping=True
    )

    # 2. 強制替換 database 模組裡的 engine
    # 這裡如果不替換，你的 App (controllers) 還是會笨笨地去連原本的真實資料庫
    database.engine = test_engine
    
    # 同時也要更新 SessionLocal，讓它產生的 session 都連到這個測試資料庫
    database.SessionLocal.configure(bind=test_engine)

    # 3. 建立 App
    app = create_app()
    app.config['TESTING'] = True

    # 4. 在這個「假資料庫」建立所有資料表 (搬家具)
    # 注意這裡用的是 test_engine
    with app.app_context():
        database.Base.metadata.create_all(bind=test_engine)

    # 5. 提供測試用的 client
    with app.test_client() as client:
        yield client

    # 6. 測試結束後清理 (拆家具)
    # 因為是記憶體資料庫，其實不 drop 也沒差，但這是好習慣
    with app.app_context():
        database.Base.metadata.drop_all(bind=test_engine)
        
    # 測試結束，記憶體釋放，一切就像沒發生過一樣