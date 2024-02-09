from flask import Blueprint, render_template, session, jsonify, request

autologout_bp = Blueprint('autologout', __name__)

@autologout_bp.route('/autologout', methods=['GET', 'POST'])
def autologout():
    if request.method == 'POST':
        # セッションからユーザー情報削除
        user_id = session.pop('user_id', None)
        user_name = session.pop('user_name', None)
        role = session.pop('role', None)

        # ユーザー情報が存在しない場合、ログアウト失敗
        if user_id is None or user_name is None or role is None:
            return jsonify({"success": False, "message": "すでにログアウトしています"})
        
        return jsonify({"success": True, "message": "正常にログアウトできました"})
    
    return render_template('index.html')
