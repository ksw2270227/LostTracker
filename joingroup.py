from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3

joingroup_bp = Blueprint('joingroup', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

def update_current_group_id(user_id, new_group_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    # ユーザーのcurrent_group_idを更新するSQL文
    update_sql = 'UPDATE users SET current_group_id = ? WHERE user_id = ?'
    cursor.execute(update_sql, (new_group_id, user_id))

    conn.commit()
    cursor.close()
    conn.close()

def update_current_group_members(group_id, group_members):
    conn = get_db_connection()
    cursor = conn.cursor()

    new_group_members = group_members + 1

    # ユーザーのcurrent_membersを更新するSQL文
    update_sql = 'UPDATE groups SET current_members = ? WHERE group_id = ?'
    cursor.execute(update_sql, (new_group_members, group_id))

    conn.commit()
    cursor.close()
    conn.close()


@joingroup_bp.route('/joingroup', methods=['GET', 'POST'])
def join_group():
    if 'user_id' not in session:
        # ユーザーがログインしていない場合、login.login_userにリダイレクト
        return redirect(url_for('login.login_user'))

    error = None
    if request.method == 'POST':
        group_id = request.form['group_id']
        password = request.form['password']
        conn = get_db_connection()
        cursor = conn.cursor()

        # セッション内のユーザーIDを取得
        user_id = session.get('user_id')

        # ユーザーのcurrent_group_idを取得
        cursor.execute('SELECT current_group_id FROM users WHERE user_id = ?', (user_id,))
        current_group_id =cursor.fetchone()[0]
       #print(f"current_group_id:{current_group_id}")
       #print(f"user_id:{user_id}")

        # グループを検索
        cursor.execute(
            'SELECT * FROM groups WHERE group_id = ? AND password = ?', (group_id, password)
        )
        group = cursor.fetchone()

        # usersテーブルでcurrent_group_idが入力idと同じものを取得
        cursor.execute('SELECT COUNT(*) FROM users WHERE current_group_id = ?', (current_group_id,))
        cursor.close()

        if group:
            # 最大人数と参加人数の比較
            if int(group[5]) <= int(group[6]):
                error = 'このグループには参加人数が最大のため参加できません。'
                test = 1
                return render_template("joingroup.html", error=error, test=test)
            # グループIDをセッションに格納
            elif current_group_id:
                # すでに別のグループに参加している場合のエラーメッセージ
                error = 'すでに別のグループに参加しています。'
                test = 1
                return render_template("joingroup.html", error=error, test=test)
            else:
                pass

            session['group_id'] = group[0]
            session['group_name'] = group[1]

            # グループに参加したユーザーのcurrent_group_idを更新
            update_current_group_id(user_id, group[0])

            # 参加したグループのcurrent_membersを更新 (group_is, current_members)
            update_current_group_members(group[0], group[6])


            # 参加成功時のリダイレクト先（例：groupページ）
            return redirect(url_for('group.group_page'))
        else:
            # 参加失敗時のエラーメッセージ
            error = '無効なグループIDまたはパスワードです。'
            test = 1
            return render_template("joingroup.html", error=error, test=test)

    # GETリクエストの場合、またはエラーがある場合に参加ページを表示.
    return render_template('joingroup.html', error=error)

    # if 'user_id' not in session:
    #     # ユーザーがログインしていない場合、login.login_userにリダイレクト
    #     return redirect(url_for('login.login_user'))

    # error = None
    # if request.method == 'POST':
    #     group_id = request.form['group_id']
    #     password = request.form['password']
    #     conn = get_db_connection()
    #     cursor = conn.cursor()

    #     # グループを検索
    #     cursor.execute(
    #         'SELECT * FROM groups WHERE group_id = ? AND password = ?', (group_id, password)
    #     )
    #     group = cursor.fetchone()
    #     cursor.close()

    #     if group:
    #         # グループIDをセッションに格納
    #         session['group_id'] = group[0]
    #         session['group_name'] = group[1]

    #         # グループに参加したユーザーのcurrent_group_idを更新
    #         user_id = session['user_id']
    #         update_current_group_id(user_id, group[0])

    #         # 参加成功時のリダイレクト先（例：groupページ）
    #         return redirect(url_for('group.group_page'))
    #     else:
    #         # 参加失敗時のエラーメッセージ
    #         error = '無効なグループIDまたはパスワードです。'
    #         test =1
    #         return render_template("joingroup.html",error=error,test=test)

    # # GETリクエストの場合、またはエラーがある場合に参加ページを表示.
    # return render_template('joingroup.html', error=error)
