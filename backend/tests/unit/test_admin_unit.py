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

# ------------------------------------------------------------------
# 測試案例 3: PUT /admin/users/<id> (成功更新)
# ------------------------------------------------------------------
@patch('controllers.admin.SessionLocal')
def test_update_user_success(mock_session_cls, client):
    """
    情境: 提供 user_id 與更新資料，API 應更新該名使用者並回傳 200。
    """
    mock_session = mock_session_cls.return_value
    
    # 1. 準備原始資料 (目前在資料庫裡的樣子)
    old_user = User(id=1, name="Old Name", email="old@test.com", address="Old City", is_driver=False, is_participating=False)
    
    # 2. 設定 Mock：當呼叫 get(1) 時回傳這筆舊資料
    mock_session.query.return_value.get.return_value = old_user

    # 3. 準備發送到 API 的更新資料
    update_payload = {
        "name": "New Name",
        "is_driver": True
    }

    # 4. 發送請求
    response = client.put('/admin/users/1', json=update_payload)

    # 5. 驗證
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == "New Name"         # 確認欄位已更新
    assert data['email'] == "old@test.com"    # 確認未提供的欄位保持原樣
    assert data['is_driver'] is True          # 確認布林值正確更新
    
    # 驗證資料庫動作
    mock_session.commit.assert_called_once()
    mock_session.close.assert_called_once()

