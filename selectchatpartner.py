from flask import Flask, render_template, request, redirect, url_for, Blueprint, session
import sqlite3
import datetime

selectchatpartner_bp = Blueprint('selectchatpartner', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@selectchatpartner_bp.route('/selectchatpartner', methods=['GET'])
def selectchatpartner():
    if(session.get('role')!='Admin'):
        return redirect(url_for('index.index'))
    users = get_users_with_latest_chat()
    return render_template('selectchatpartner.html', users=users)

def get_users_with_latest_chat():
    try:
        # session['user_id'] = 2
        # session['role'] ='Admin'
        # session['user_name'] = 'Admin2'
       
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # 各ユーザーとAdminとの最新のチャット情報を取得
        cursor.execute('''
            SELECT 
                users.user_id, 
                users.user_name, 
                MAX(messages.sent_time) as latest_chat_time, 
                messages.message_content as latest_chat_content
            FROM 
                users 
            LEFT JOIN 
                messages ON (
                    (users.user_id = messages.sender_user_id AND messages.receiver_user_id = 2) OR
                    (users.user_id = messages.receiver_user_id AND messages.sender_user_id = 2)
                )
            GROUP BY 
                users.user_id
        ''')
        # ユーザーID = 送信者ID     受信者ID = 2 (User -> Admin)
        # ユーザーID = 受信者ID     送信者ID = 2 (Admin -> User)

        users = []
        for row in cursor.fetchall():
            user = {
                'user_id': row[0],
                'user_name': row[1],
                'latest_chat_time': row[2] if row[2] is not None else 'N/A',
                'latest_chat_content': row[3] if row[3] is not None else 'チャット履歴なし'
            }
            users.append(user)

        cursor.close()
        conn.close()

        return users
    except Exception as e:
        print(f"ユーザーと最新のチャットを取得する際にエラーが発生しました: {e}")
        return None