from flask import Flask, render_template, request, redirect, url_for, Blueprint, session, g
import sqlite3
import datetime

chat_bp = Blueprint('chat', __name__)
app = Flask(__name__)


def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn


@chat_bp.route('/chat', methods=['GET', 'POST'])
def chat():
    # ユーザーIDがセッションに存在しない場合、ログインページにリダイレクト
    if session.get('user_id') is None:
        return redirect(url_for('login.login_user'))
    
    if(session.get('role')=='Admin'):
        return redirect(url_for('selectchatpartner.selectchatpartner'))
    
    sender_role = session.get('role')
    if sender_role == 'Admin':
        # URLからクエリパラメータとして渡されたuser_idを取得し、int型に変換
        if request.method == 'POST':
            select_user_id = int(request.form.get('user_url_id'))
            session['user_url_id'] = select_user_id
        elif request.method == 'GET':
            select_user_id = int(request.args.get('user_url_id'))
            session['user_url_id'] = select_user_id
        else:
            select_user_id = 11
            session['user_url_id'] = select_user_id

    # if request.method == 'POST':
    #     select_user_id = int(request.form['user_url_id'])
    # elif request.method == 'GET':
    #     select_user_id = int(request.args['user_url_id'])
    # else:
    #      select_user_id = 11

    

    if request.method == 'POST':
        message_content = request.form['message_content']
        receiver_user_id = session.get('user_url_id')

        if message_content.strip() != '':
            sender_user_id = session.get('user_id')
            # sender_role = session.get('role')
            
            # 管理者へのメッセージ送信 送信先をAdminの2に固定
            if sender_role == 'User':
                receiver_user_id = 2
                receiver_role = 'Admin'
            elif sender_role == 'Admin':
            # 管理者がメッセージを送信する場合の処理
                receiver_user_id = session.get('user_url_id')#
                receiver_role = 'User'

            sent_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            save_message_to_database(sender_user_id, sender_role, receiver_user_id, receiver_role, message_content, sent_time)

            if sender_role == 'Admin':
                return redirect(url_for('chat.chat', user_url_id=receiver_user_id))
            else:
                return redirect(url_for('chat.chat'))

    chat_history = get_chat_history()
    if sender_role == 'Admin':
        return render_template('chat.html', chat_history=chat_history,user_url_id=select_user_id)
    else:
        return render_template('chat.html', chat_history=chat_history)

def save_message_to_database(sender_user_id, sender_role, receiver_user_id, receiver_role, message_content, sent_time):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('INSERT INTO messages (sender_user_id, sender_role, receiver_user_id, receiver_role, message_content, sent_time) VALUES (?, ?, ?, ?, ?, ?)',
                    (sender_user_id, sender_role, receiver_user_id, receiver_role, message_content.strip(), sent_time))

    conn.commit()
    cursor.close()
    conn.close()

def get_chat_history():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        receiver_user_id = session.get('user_url_id')
        sender_user_id = session.get('user_id')
        sender_role = session.get('role')

        # URLからクエリパラメータとして渡されたuser_idを取得
        # select_user_id = int(request.args.get('user_url_id')) if request.args.get('user_url_id') else None

        

        if sender_role == 'User':
            # ユーザーとしての履歴を取得 sender_user_id/roleを2/Adminに
            cursor.execute('SELECT * FROM messages WHERE (sender_user_id = ? AND sender_role = ? AND receiver_user_id = ? AND receiver_role = ?) OR (sender_user_id = ? AND sender_role = ? AND receiver_user_id = ? AND receiver_role = ?)',
                (sender_user_id, sender_role, 2, 'Admin', 2, 'Admin', sender_user_id, sender_role))
        elif sender_role == 'Admin':
            # 管理者としての履歴を取得　receiver_roleをUserに
            cursor.execute('SELECT * FROM messages WHERE (sender_user_id = ? AND sender_role = ? AND receiver_user_id = ? AND receiver_role = ?) OR (sender_user_id = ? AND sender_role = ? AND receiver_user_id = ? AND receiver_role = ?)',
                (sender_user_id, sender_role, receiver_user_id, 'User', receiver_user_id, 'User', sender_user_id, sender_role))

        chat_history = cursor.fetchall()

        cursor.close()
        conn.close()

        return chat_history
    except Exception as e:
        print(f"Error fetching chat history: {e}")
        return None
    
if __name__ == '__main__':
    app.run(debug=True)