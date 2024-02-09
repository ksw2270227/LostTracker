from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import sqlite3
from flask import jsonify


eventparticpation_bp = Blueprint('eventparticpation', __name__)

def get_db_connection():
    conn = sqlite3.connect('testDB.db')
    return conn

@eventparticpation_bp.route('/eventparticpation', methods=['GET', 'POST'])
def eventparticpation():
    # ログインしていればeventparticpationを表示
    if session.get('user_id') is None:
        return redirect(url_for('login.login_user'))
    elif session.get('user_id'):
        return redirect(url_for('event.event'))
    else:
        return render_template("eventparticpation.html")