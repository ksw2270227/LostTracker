from flask import Flask, render_template, jsonify, Blueprint,request,session,redirect,url_for
import sqlite3
check_data_bp = Blueprint('check_data', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

def show_tables():
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

    return render_template('check_data.html', users=users,admins=admins ,companies=companies,companies_employee=companies_employee,groups=groups,events=events,messages=messages,location_data=location_data,location_history=location_history)


@check_data_bp.route('/check_data')
def check_data():
    if(session.get('role')!='Admin'):
        return redirect(url_for('index.index'))
    
    return show_tables()

@check_data_bp.route('/edit_row', methods=['POST'])
def edit_row():
    data = request.json
    table = data['table']
    row_id = data['id']
    row_data = data['data']

    # データベース接続と行の更新
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # 更新クエリの構築（注意: SQLインジェクションを避けるために、パラメータ化されたクエリを使用）
        # 例: UPDATE users SET user_name = ?, email = ? WHERE user_id = ?
        query = f'UPDATE {table} SET ' + ', '.join([f"{key} = ?" for key in row_data.keys()]) + f' WHERE user_id = ?'
        cur.execute(query, list(row_data.values()) + [row_id])
        conn.commit()

        cur.close()
        conn.close()
        return jsonify({'message': 'データが正常に更新されました。'})
    except Exception as e:
        return jsonify({'message': f'更新中にエラーが発生しました: {e}'})