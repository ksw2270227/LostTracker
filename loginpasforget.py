from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask import Blueprint

loginpasforget_bp = Blueprint('loginpasforget', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

@loginpasforget_bp.route('/loginpasforgetchange.html', methods=['POST'])
def loginpasforget_change():
    if request.method == 'POST':
        email = request.form['emailAddressInput']

        # パスワードのハッシュ化はセキュリティ上の理由で必要ですが、
        # この例では簡略化のため省略しています。実際には適切なハッシュ関数を使用してください。

        conn = get_db_connection()
        cursor = conn.cursor()

        # ユーザーが存在するか確認
        cursor.execute('SELECT * FROM users WHERE email_address = %s', (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            # ここで新しいパスワードを設定するなどの処理を行います。
            # この例では省略しています。

            return render_template('loginpasforgetchange.html', message='パスワードの変更が完了しました。')

        # ユーザーが存在しない場合の処理を行うか、
        # ユーザーに通知してください。

        cursor.close()
        conn.close()

        return redirect(url_for('loginpasforgetchange.html'))

    return render_template('loginpasforget.html', message='メールアドレスが見つかりませんでした。')

# この部分でアプリケーションにBlueprintを登録します。
# app.register_blueprint(loginpasforget_bp)  # app.pyで行うことが一般的
