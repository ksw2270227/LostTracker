from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from flask import Blueprint

creategroup_bp = Blueprint('creategroup', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@creategroup_bp.route('/creategroup', methods=['GET', 'POST'])
def create_group():
    if 'user_id' not in session:
        # ユーザーがログインしていない場合、login.login_userにリダイレクト
        return redirect(url_for('login.login_user'))

    if request.method == 'POST':
        print("formからデータを取得します")
        # フォームからデータを受け取り
        group_name = request.form['group_name']
        password = request.form['password']
        max_members = request.form['man']  # フォームの input 要素の名前が 'man' なのでこちらを指定

        # マイナスでないことを確認
        if len(max_members) < 0:
            return render_template('creategroup.html', error="参加人数は0以上の整数で入力してください")

        # データベースに挿入する処理
        conn = get_db_connection()
        cursor = conn.cursor()
        user_id = session.get('user_id')  # セッションからユーザーIDを取得

        # 追加: 一意の制約を追加する
        try:
            cursor.execute('SELECT group_id FROM groups WHERE user_id = ?', (user_id,))
            existing_group = cursor.fetchone()
            print(f"existing_group:{existing_group}")

            #groupテーブルにデータを挿入
            cursor.execute(
                'INSERT INTO groups (group_name, password, user_id, creation_date, max_members, current_members, event_id) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (group_name, password, user_id, '2023-01-17 12:00:00', max_members, 0, 0)
            )
            # 追加: 作成したグループの group_id を取得
            cursor.execute('SELECT group_id FROM groups WHERE user_id = ?', (user_id,))
            group_id = cursor.fetchone()[0]

            # 追加: users テーブルの current_group_id を更新
            cursor.execute('UPDATE users SET current_group_id = ? WHERE user_id = ?', (group_id, user_id))

            #2/6に追加したところ
            if existing_group:
            # 既に同じ user_id を持つグループが存在する場合の処理
                return render_template('creategroup.html', error="同じユーザーIDで既にグループが作成されています")
            #ここまで
        except sqlite3.IntegrityError as e:
            # 重複がある場合の処理
            print("追加: 重複があります。")
            conn.rollback()
        else:
            # 重複がない場合の処理
            print("追加: 成功")
            conn.commit()
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('group.group_page'))  # 仮に/indexにリダイレクト
    
    return render_template('creategroup.html')  # グループ作成フォームを表示
