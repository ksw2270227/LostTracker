# autologin.py
from flask import Blueprint, jsonify, session

auto_login_bp = Blueprint('auto_login', __name__)

@auto_login_bp.route("/auto-login", methods=["POST"])
def auto_login():
    if 'user_id' in session:
        # セッションにユーザーIDが存在する場合、すでにログインしていると判断
        return jsonify({'user_name': session.get('user_name'), 'user_id': session.get('user_id'), 'message': 'すでにログインしています。'})
    else:
        # 通常はここでユーザー認証を行いますが、デモのために固定値を使用
        session['user_id'] = 2
        session['user_name'] = 'taro@example.com'
        session['role'] = 'User'
        return jsonify({'user_name': session.get('user_name'), 'user_id': session.get('user_id'), 'message': 'ログイン成功！'})
