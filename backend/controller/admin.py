# backend/controller/admin.py

from flask import Blueprint, jsonify
from models import User # 匯入 Model
from database import SessionLocal # 匯入 DB Session
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    """
    在經典 MVC 中, Controller 直接與 Model 互動來獲取資料。
    """
    db = SessionLocal() 
    try:
        # 直接在 Controller 內部執行資料庫查詢
        users = db.query(User).all()

        user_list = []
        for user in users:
            # 將 Model 物件轉換為 JSON 友好的字典格式
            user_list.append({
                'id': user.id,
                'name': user.name,
                'email': user.email,
                'address': user.address,
                'is_driver': user.is_driver,
                'is_participating': user.is_participating,
            })
        
        return jsonify(user_list), 200

    except SQLAlchemyError as e:
        print(f"Database error: {e}")
        return jsonify({"message": "Database operation failed", "details": str(e)}), 500
    except Exception as e:
        return jsonify({"message": "An unexpected server error occurred", "details": str(e)}), 500
    finally:
        db.close() # 關閉 Session