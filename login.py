from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask import jsonify


login_bp = Blueprint('login', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@login_bp.route('/login', methods=['GET', 'POST'])
def login_user():

    if 'user_id' in session:
        return redirect(url_for('index.index'))

    error = None
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーを検索
        cursor.execute(
            'SELECT * FROM users WHERE email_address = ? AND password = ?',(email_address, password)
        )
        user = cursor.fetchone()
        print(user)
        cursor.close()
        conn.close()

        if user:
            # ユーザーIDをセッションに格納
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            session['role']='User'
            # ログイン成功時のリダイレクト先（例：indexページ）
            return redirect(url_for('index.index'))
        else:
            # ログイン失敗時のエラーメッセージ
            error = '無効なメールアドレスまたはパスワードです。'
            test =1
            return render_template("login.html",error=error,test=test)
    else :
        return render_template("login.html")     

@login_bp.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    error = None
    if request.method == 'POST':
        email_address = request.form['email_address']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()

        # 管理者を検索
        cursor.execute(
            'SELECT * FROM admins WHERE email_address = ? AND password = ?', (email_address, password)
        )
        admin = cursor.fetchone()
        cursor.close()
        conn.close()

        if admin:
            # 管理者IDをセッションに格納
            session['user_id'] = admin[0]
            session['user_name'] = admin[1]
            session['role'] = 'Admin'  # ロールをAdminに設定
            # ログイン成功時のリダイレクト先（例：indexページ）
            return redirect(url_for('index.index'))
        else:
            # ログイン失敗時のエラーメッセージ
            error = '無効なメールアドレスまたはパスワードです。'
            return render_template("login_admin.html", error=error)
    else:
        return render_template("login_admin.html")
