from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3

event_bp = Blueprint('event', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

# イベント表示関数
def event_show(event):
    if event:
        event_id = event[2]  # イベントIDを取得
        session['event_id'] = event_id  # イベントIDをセッションに保存

        event_name = event[1]
        start_time = event[4]
        end_time = event[5]
        location = event[6]
        event_content = event[7]
        
        return render_template("event.html", event_name=event_name, start_time=start_time,
                               end_time=end_time, location=location, event_content=event_content)
    else:
        flash('イベントが見つかりませんでした。')  # エラーメッセージをフラッシュ
        errorid = 1
        return render_template("eventparticpation.html",errorid=errorid)  # eventparticpationへリダイレクト

@event_bp.route('/event', methods=['GET', 'POST'])
def event():
    if request.method == 'POST':
        if session.get('user_id') is None:
            return redirect(url_for('login.login_user'))
        
        # イベント参加画面のformから取得
        event_id = request.form['eventidinput']
        password = request.form['passwordinput']

        conn = get_db_connection()
        cursor = conn.cursor()

        # 入力イベントIDと一致するイベントを検索
        cursor.execute('SELECT * FROM events WHERE event_id = ? AND password = ?', (event_id, password))
        event = cursor.fetchone()

        if event:
            # イベントに参加できた場合、ユーザーのcurrent_event_idを更新
            user_id = session.get('user_id')
            cursor.execute("UPDATE users SET current_event_id = ? WHERE user_id = ?", (event_id, user_id))
            conn.commit()

        cursor.close()
        conn.close()

        return event_show(event)
    else:  # GET request # メニューからイベントへ
        # ログインしていなければログイン画面へリダイレクト
        if session.get('user_id') is None:
            return redirect(url_for('login.login_user'))
        
        # イベントに参加していなければイベント参加画面へ
        if session.get('event_id') is None:
            return render_template("eventparticpation.html")
        
        event_id = session.get('event_id')
        
        conn = get_db_connection()
        cursor = conn.cursor()

        # 入力イベントIDと一致するイベントを検索
        cursor.execute('SELECT * FROM events WHERE event_id = ?', (event_id,))
        event = cursor.fetchone()

        cursor.close()
        conn.close()

        return event_show(event)


# イベント退出処理
@event_bp.route('/exit_event', methods=['POST'])
def exit_event():
    if session.get('user_id') is None:
        return jsonify({'error': 'ログインしていません'}), 401
    # flash_message = '<div class="alert alert-danger">ログインしていません</div>'
    #     return render_template('your_template.html', flash_message=flash_message), 401

    current_event_id = session.get('event_id')
    if current_event_id is not None:
        user_id = session.get('user_id')
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET current_event_id = 0 WHERE user_id = ?", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        session.pop('event_id')
        return 'OK', 200
    else:
        return jsonify({'error': 'イベントに参加していません'}), 400
