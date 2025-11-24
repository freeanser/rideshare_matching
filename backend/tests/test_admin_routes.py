# backend/tests/test_admin_routes.py

import json
# from app import create_app
# from ..app import create_app
# from backend.app import create_app
from ..app import create_app

def test_get_all_users():
    app = create_app()
    client = app.test_client()

    response = client.get("/admin/users")
    assert response.status_code == 200

    data = json.loads(response.data)
    assert isinstance(data, list)

    if data:  # if there's at least one user
        user = data[0]
        assert "id" in user
        assert "name" in user
        assert "email" in user
        assert "address" in user
        assert "is_driver" in user
        assert "is_participating" in user
