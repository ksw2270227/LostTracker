from flask import Flask, render_template, request, redirect, url_for, Blueprint
import mysql.connector

eventlist_bp = Blueprint('eventlist', __name__)

def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        database='testDB1',
        user='root',
        password='pass'
    )

def insert_event(event_name, start_time, end_time, location, event_content):
    connection =  get_db_connection()
    cursor = connection.cursor()

    # イベント情報をINSERT
    insert_query = """
        INSERT INTO events (event_name, start_time, end_time, location, event_content)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = (event_name, start_time, end_time, location, event_content)
    cursor.execute(insert_query, data)

    connection.commit()
    cursor.close()
    connection.close()

@eventlist_bp.route('/submit_event', methods=['POST'])
def submit_event():
    if request.method == 'POST':
        # フォームからデータを取得
        event_name = request.form['event_name']
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        location = request.form['location']
        event_content = request.form['event_content']

        # データベースにイベント情報を挿入
        insert_event(event_name, start_time, end_time, location, event_content)

        return redirect(url_for('eventlist.show_events'))

@eventlist_bp.route('/show_events')
def show_events():
    # データベースからイベント一覧を取得
    connection =  get_db_connection()
    cursor = connection.cursor()

    select_query = 'SELECT * FROM events'
    cursor.execute(select_query)
    events = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template('eventlist.html', events=events)