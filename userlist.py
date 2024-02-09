from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask import Blueprint

userlist_bp = Blueprint('userlist', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@userlist_bp.route('/userlist', methods=['GET', 'POST'])
def userlist():
    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        # 入力フォームに合わせて他の情報も取得

        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザー情報をusersテーブルに挿入するクエリ
        insert_query = "INSERT INTO users (user_name, full_name) VALUES (%s, %s)"
        cursor.execute(insert_query, (username, full_name))  # 他の情報も追加

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('userlist.userlist'))  # データベースに挿入後にリダイレクト

    return render_template('userlist.html')

if __name__ == "__main__":
    app = Flask(__name__)
    app.register_blueprint(userlist_bp)
    app.run(debug=True)
