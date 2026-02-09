# backend/tests/unit/test_admin_unit.py
import pytest
from unittest.mock import patch
from sqlalchemy.exc import SQLAlchemyError
# 重點：直接 Import 真正的 Model，確保測試資料結構正確
from models import User 

# ------------------------------------------------------------------
# 測試案例 1: GET /admin/users (成功取得列表)
# ---------------------------------------------------------------
# patch 的路徑必須是你 controller 檔案中 "匯入 SessionLocal 的位置"
@patch('controllers.admin.SessionLocal') 
def test_get_all_users_success(mock_session_cls, client):
    """
    情境: 資料庫裡有兩個使用者, API 應該回傳這兩筆資料。
    """
    mock_session = mock_session_cls.return_value
    
    # 【優點】直接使用 User Model，如果欄位打錯字，IDE 會提示你，且結構與專案一致
    # 注意：這裡只是在記憶體中建立物件，並沒有寫入資料庫，所以是合法的 Unit Test
    fake_users = [
        User(id=1, name="Alice", email="alice@test.com", address="Taipei", is_driver=True, is_participating=True),
        User(id=2, name="Bob", email="bob@test.com", address="Tainan", is_driver=False, is_participating=True)
    ]

    # 設定當呼叫 all() 時，回傳上面做好的假資料
    mock_session.query.return_value.all.return_value = fake_users

    response = client.get('/admin/users')

    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2
    assert data[0]['name'] == "Alice"
    assert data[1]['email'] == "bob@test.com"
    
    mock_session.close.assert_called_once()


# ------------------------------------------------------------------
# 測試案例 2: GET /admin/users (資料庫發生預期外的錯誤)
# ------------------------------------------------------------------
@patch('controllers.admin.SessionLocal')
def test_get_all_users_db_error(mock_session_cls, client):
    """
    情境: 資料庫連線失敗或查詢錯誤, API 應該優雅地回傳 500。
    """
    mock_session = mock_session_cls.return_value
    mock_session.query.side_effect = SQLAlchemyError("Connection failed")

    response = client.get('/admin/users')

    assert response.status_code == 500
    assert "Database operation failed" in response.get_json()['message']
    mock_session.close.assert_called_once()
