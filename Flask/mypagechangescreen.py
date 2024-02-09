from flask import Flask, render_template, request, redirect, url_for, Blueprint
import mysql.connector

mypagechangescreen_bp = Blueprint('mypagechangescreen', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@mypagechangescreen_bp.route('/mypagechangescreen', methods=['GET', 'POST'])
def mypage_changescreen():
    if request.method == 'POST':
        # フォームからのデータを取得
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        current_password = request.form['currentPassword']
        new_password = request.form['newPassword']
        age = request.form['age']
        gender = request.form['gender']

        # データベースに接続
        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザー情報を更新するSQLクエリを実行
        update_query = """
        UPDATE users
        SET name = %s, phone_number = %s, email_address = %s,
            current_password = %s, new_password = %s, age = %s, gender = %s
        WHERE user_id = %s
        """
        user_id = 1  # 仮にユーザーIDを1としています。実際のユーザーIDに置き換えてください。
        cursor.execute(update_query, (name, phone, email, current_password, new_password, age, gender, user_id))

        # データベースの変更をコミット
        conn.commit()

        # データベース接続をクローズ
        cursor.close()
        conn.close()

        # 更新が完了したらマイページにリダイレクト
        return redirect(url_for('mypage_changescreen'))

    # GETリクエストの場合はマイページ変更画面を表示
    return render_template('mypagechangescreen.html')

