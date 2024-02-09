from flask import Blueprint, render_template, session
import sqlite3

index_bp = Blueprint('index',__name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@index_bp.route("/index")
def index():
    user_id = session.get('user_id')
    user_name = session.get('user_name')

    # user_idがセッションにあるがuser_nameがない場合、データベースから取得する
    if user_id and not user_name:
        conn = get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT user_name FROM users WHERE user_id = ?', (user_id,))
            user = cursor.fetchone()
            user_name = user[0] if user else None
        except Exception as e:
            print(f"Database error: {e}")
        finally:
            conn.close()

    print(f"user_name: {user_name}  user_id: {user_id}")
    return render_template("index.html", user_name=user_name, user_id=user_id)
