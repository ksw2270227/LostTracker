from flask import Blueprint, render_template, session, request, jsonify, redirect, url_for
import sqlite3
import datetime

map_bp = Blueprint('map', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@map_bp.route('/map')
def show_map():
    user_id = session.get('user_id')
    if user_id:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT current_latitude, current_longitude FROM location_data WHERE user_id = ?', (user_id,))
        location = cursor.fetchone()
        cursor.close()
        conn.close()

        if location:
            # ユーザーの位置情報が存在する場合
            return render_template('map.html', latitude=location[0], longitude=location[1],login_user_id=user_id)
        else:
            return render_template('map.html',login_user_id=user_id)
    else:
        return redirect(url_for('login.login_user'))

@map_bp.route('/api/update-user-status', methods=['POST'])
def update_user_status():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.json
    status = data.get('status')

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # usersテーブルのuser_statusを更新
        cursor.execute('UPDATE users SET user_status = ? WHERE user_id = ?', (status, user_id))

        # location_dataテーブルのuser_statusを更新
        cursor.execute('UPDATE location_data SET user_status = ? WHERE user_id = ?', (status, user_id))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500

    cursor.close()
    conn.close()
    return jsonify({'message': 'User status updated successfully'})


@map_bp.route('/api/update-location', methods=['POST'])
def update_location():

    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    data = request.json
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    altitude = data.get('altitude', 0)  # デフォルト値は0
    acquisition_time = datetime.datetime.now()  # 現在の時刻を取得

    # データベース接続
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # users テーブルからユーザーステータスを取得
        cursor.execute('SELECT user_status FROM users WHERE user_id = ?', (user_id,))
        user_status_result = cursor.fetchone()
        user_status = user_status_result[0] if user_status_result else 'unknown'

        # location_data テーブルの更新
        cursor.execute('''
            INSERT INTO location_data (user_id, user_status, current_latitude, current_longitude, current_altitude, acquisition_time)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
            user_status = excluded.user_status,
            current_latitude = excluded.current_latitude,
            current_longitude = excluded.current_longitude,
            current_altitude = excluded.current_altitude,
            acquisition_time = excluded.acquisition_time;
        ''', (user_id, user_status, latitude, longitude, altitude, acquisition_time))

        # location_history テーブルへの挿入
        cursor.execute('''
            INSERT INTO location_history (user_id, latitude, longitude, altitude, acquisition_time, user_status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (user_id, latitude, longitude, altitude, acquisition_time, user_status))

        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        cursor.close()
        conn.close()
        return jsonify({'error': str(e)}), 500
    cursor.close()
    conn.close()
    return jsonify({'message': 'Location updated successfully'})

@map_bp.route('/api/get-user-status')
def get_user_status():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'User not logged in'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT user_status FROM users WHERE user_id = ?', (user_id,))
        user_status = cursor.fetchone()
        if user_status:
            return jsonify({'user_status': user_status[0]})
        else:
            return jsonify({'error': 'User not found'}), 404
    except sqlite3.Error as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

#新しく追加した機能
@map_bp.route('/api/get-group-users')
def get_group_users():
    user_id = session.get('user_id')
    if not user_id:
        # print("User not logged in")
        # return jsonify({'error': 'User not logged in'}), 401
        return redirect(url_for('login.login_user'))

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 現在のユーザーのグループIDを取得
        cursor.execute('SELECT current_group_id FROM users WHERE user_id = ?', (user_id,))
        group_id = cursor.fetchone()[0]
        # print("Group ID:", group_id)

        # 同じグループの全ユーザー情報を取得
        cursor.execute('''
            SELECT u.user_id, u.full_name, l.current_latitude, l.current_longitude, l.user_status
            FROM users u
            JOIN location_data l ON u.user_id = l.user_id
            WHERE u.current_group_id = ?
        ''', (group_id,))
        users = cursor.fetchall()
        # print("Group users:", users)

        # 各ユーザーに対して位置情報を取得
        user_locations = []
        for user in users:
            cursor.execute('SELECT current_latitude, current_longitude, user_status FROM location_data WHERE user_id = ?', (user[0],))
            location_data = cursor.fetchone()
            if location_data:
                user_locations.append((user[0], user[1], *location_data))

        # 出力
        # for location in user_locations:
        #     print(f"({location[0]}, '{location[1]}', {location[2]}, {location[3]}, '{location[4]}')")

        return jsonify({'group_users': user_locations})
    except sqlite3.Error as e:
        # print("Database error:", str(e))
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

