from flask import Blueprint, render_template, session, jsonify, request, redirect, url_for

logout_bp = Blueprint('logout', __name__)

@logout_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    if request.method == 'POST':
        # セッションからユーザー情報削除
        user_id = session.pop('user_id', None)
        user_name = session.pop('user_name', None)
        role = session.pop('role', None)

        # ユーザー情報が存在しない場合、ログアウト失敗
        if user_id is None or user_name is None or role is None:
            return jsonify({"success": False, "message": "Logout failed"})
        
        return jsonify({"success": True, "message": "Logout successful"})
    
# ログインしていない場合、login.login_userにリダイレクト
    return redirect(url_for('login.login_user'))