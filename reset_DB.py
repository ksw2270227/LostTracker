import os
print("Current Directory:", os.getcwd())

from flask import Flask, render_template, Blueprint,jsonify
import sqlite3

reset_DB_bp = Blueprint('reset_DB', __name__)

def reset_db():
    db_path = 'testDB.db'
    if os.path.exists(db_path):
        os.remove(db_path)

    # データベースファイルが存在しない場合、新しいデータベースが自動的に作成される
    conn = sqlite3.connect(db_path)
    return conn

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

def create_db_from_sql(sql_file_path):
    conn = reset_db()  # 新しいデータベースファイルを作成
    cur = conn.cursor()

    with open(sql_file_path, 'r', encoding='utf-8') as sql_file:
        sql_script = sql_file.read()

    cur.executescript(sql_script)
    conn.commit()
    cur.close()
    conn.close()

@reset_DB_bp.route('/reset_DB', methods=["POST"])
def show_tables():
    create_db_from_sql('sql/init.sql')  # 最初にデータベースをリセットして初期化

    conn = get_db_connection()  # リセット後のデータベースに接続
    cur = conn.cursor()

    # users テーブルのデータを取得
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()

    # admins テーブルのデータを取得
    cur.execute('SELECT * FROM admins')
    admins = cur.fetchall()

    # [companies]テーブルのデータを取得
    cur.execute('SELECT * FROM  companies')
    companies = cur.fetchall()
    
    # [companies_employee]テーブルのデータを取得
    cur.execute('SELECT * FROM companies_employee')
    companies_employee  = cur.fetchall()
    
    # [groups]テーブルのデータを取得
    cur.execute('SELECT * FROM groups')
    groups  = cur.fetchall()
    
    # [events]テーブルのデータを取得
    cur.execute('SELECT * FROM events')
    events  = cur.fetchall()
    
    # [messages]テーブルのデータを取得
    cur.execute('SELECT * FROM messages')
    messages  = cur.fetchall()
    
    # [location_data]テーブルのデータを取得
    cur.execute('SELECT * FROM location_data')
    location_data  = cur.fetchall()
    
    # [location_history]テーブルのデータを取得
    cur.execute('SELECT * FROM location_history')
    location_history  = cur.fetchall()

    cur.close()
    conn.close()

    # ポップアップメッセージを設定
    popup_message = "データベースがリセットされました。"

    return jsonify({'message': popup_message})

