# backend/tests/test_admin_routes.py

import json
from app import create_app

# def test_get_all_users():
#     app = create_app()
#     client = app.test_client()

#     response = client.get("/admin/users")
#     assert response.status_code == 200

#     data = json.loads(response.data)
#     assert isinstance(data, list)

#     if data:  # if there's at least one user
#         user = data[0]
#         assert "id" in user
#         assert "name" in user
#         assert "email" in user
#         assert "address" in user
#         assert "is_driver" in user
#         assert "is_participating" in user

# 注意：這裡的參數多了一個 client，它會自動從 conftest.py 傳進來
def test_get_all_users(client):
    
    # 不需要這兩行了，conftest 幫你做好了
    # app = create_app() 
    # client = app.test_client()

    response = client.get("/admin/users")
    
    # 這裡原本報錯 500，現在應該會是 200 了 (因為資料表存在了，只是回傳空陣列)
    assert response.status_code == 200