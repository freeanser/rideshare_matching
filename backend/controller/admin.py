# backend/controller/admin.py

from flask import Blueprint, jsonify, request
from models import User 
from database import SessionLocal 
from sqlalchemy.exc import SQLAlchemyError

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/users', methods=['GET'])
def get_all_users():
    db = SessionLocal() 
    try:
        users = db.query(User).all()

        user_list = []
        for user in users:
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
        db.close()

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """
    Update an existing user. This will be called by the Admin page inline edit.
    """
    db = SessionLocal()
    try:
        data = request.get_json()

        user = db.query(User).get(user_id)
        if not user:
            return jsonify({"message": f"User with id {user_id} not found"}), 404

        # Only update allowed fields if they are provided in the request body
        if 'name' in data:
            user.name = data['name']
        if 'email' in data:
            user.email = data['email']
        if 'address' in data:
            user.address = data['address']
        if 'is_driver' in data:
            user.is_driver = data['is_driver']
        if 'is_participating' in data:
            user.is_participating = data['is_participating']

        db.commit()

        return jsonify({
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'address': user.address,
            'is_driver': user.is_driver,
            'is_participating': user.is_participating,
        }), 200

    except SQLAlchemyError as e:
        db.rollback()
        print(f"Database error: {e}")
        return jsonify({"message": "Database operation failed", "details": str(e)}), 500
    except Exception as e:
        db.rollback()
        return jsonify({"message": "An unexpected server error occurred", "details": str(e)}), 500
    finally:
        db.close()

