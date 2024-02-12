# group.py

from flask import Blueprint, render_template, session, jsonify, current_app, redirect, url_for
import sqlite3

group_bp = Blueprint('group', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

# joingroup成功時ここに遷移
@group_bp.route('/group', methods=['GET'])
def group_page():
    user_id = session.get('user_id')

    if user_id is not None:
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # ログインユーザーに参加しているグループがあるか
            cursor.execute('SELECT current_group_id FROM users WHERE user_id = ?', (user_id,))
            current_group_id = cursor.fetchone()

            if current_group_id:
                current_group_id = current_group_id[0]

                # 参加グループidが0または無い場合joingroupに戻る
                if current_group_id == 0 or current_group_id is None:
                    # current_group_idが0もしくはNoneの場合、/joingroupにリダイレクト
                    return redirect(url_for('joingroup.join_group'))

                 # 参加グループidと同じgroupsテーブルの列をすべて取得
                cursor.execute('SELECT * FROM groups WHERE group_id = ?', (current_group_id,))
                group = cursor.fetchone()

                # グループが欠けなく入ったら
                if group:
                    group_data = {
                        'group_name': group[1],
                        'group_id': group[0],
                        'max_members': group[5],
                        'current_members':group[6]
                    }

                    # 参加者数を取得
                    cursor.execute('SELECT current_members FROM groups WHERE group_id = ?', (current_group_id,))
                    group_count = cursor.fetchone()[0]

                    # 参加者のリストを取得
                    cursor.execute('SELECT full_name FROM users WHERE current_group_id = ?', (current_group_id,))
                    participants = [{'full_name': row[0]} for row in cursor.fetchall()]

                    # 参加者数と参加者名とともにgroup.htmlにとぶ
                    return render_template('group.html', group=group_data, group_count=group_count, participants=participants)
                else:
                    # 見つからない場合それぞれにNoneをいれgroup.htmlにとぶ
                    return render_template('group.html', group=None, group_count=None, participants=None)
            else:
                return jsonify({'success': False, 'error': 'ユーザーはグループに所属していません'})
        except Exception as e:
            current_app.logger.error(f"Error fetching group data: {str(e)}")
            return jsonify({'success': False, 'error': str(e)})
        finally:
            cursor.close()
            conn.close()
    else:
        return redirect(url_for('login.login_user'))
    
@group_bp.route('/leavegroup', methods=['POST'])
def leave_group():
    user_id = session.get('user_id')
    if user_id is None:
        return jsonify({'success': False, 'error': 'ユーザーがログインしていません'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ユーザーの現在のグループIDを取得
        cursor.execute('SELECT current_group_id FROM users WHERE user_id = ?', (user_id,))
        current_group_id = cursor.fetchone()
        if current_group_id is None or current_group_id[0] == 0:
            return jsonify({'success': False, 'error': 'ユーザーはグループに所属していません'}), 404

        current_group_id = current_group_id[0]

        # ユーザーのcurrent_group_idを0に設定して退会処理
        cursor.execute('UPDATE users SET current_group_id = 0 WHERE user_id = ?', (user_id,))
        conn.commit()

        # groupsテーブルから現在のメンバー数を取得して更新
        cursor.execute('SELECT current_members FROM groups WHERE group_id = ?', (current_group_id,))
        current_members = cursor.fetchone()
        if current_members is None:
            return jsonify({'success': False, 'error': 'グループが存在しません'}), 404

        current_members = current_members[0] - 1
        if current_members > 0:
            # メンバー数を更新
            cursor.execute('UPDATE groups SET current_members = ? WHERE group_id = ?', (current_members, current_group_id))
        else:
            # メンバーがいなくなったらグループを削除
            cursor.execute('DELETE FROM groups WHERE group_id = ?', (current_group_id,))

        conn.commit()
        return jsonify({'success': True, 'message': 'グループから正常に退会しました'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
