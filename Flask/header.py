from flask import Blueprint, render_template, session

index_bp = Blueprint('index', __name__)

signup_bp = Blueprint('signup', __name__)
login_bp = Blueprint('login', __name__)

mypage_bp = Blueprint('mypage', __name__)
chat_bp = Blueprint('chat', __name__)
group_bp = Blueprint('group', __name__)
map_bp = Blueprint('map', __name__)
logout_bp = Blueprint('logout', __name__)

header_bp = Blueprint('header', __name__)

# # ルート設定
# @index_bp.route('/index', methods=['GET', 'POST'])
# def index():
#     user_id = int(session.get('user_id'))
#     print(f"user_id: {user_id}")
#     return render_template('header.html', user_id=user_id)

# # 未ログイン
# @signup_bp.route('/signup', methods=['GET', 'POST'])
# def signup():
#     user_id = int(session.get('user_id'))
#     print(f"user_id: {user_id}")
#     return render_template('header.html', user_id=user_id)

# @login_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     user_id = int(session.get('user_id'))
#     print(f"user_id: {user_id}")
#     return render_template('header.html', user_id=user_id)




# ログイン済み
@header_bp.route('*', methods=['GET', 'POST'])
def header():
    user_id = int(session.get('user_id'))
    print(f"user_id: {user_id}")
    return render_template('header.html', user_id=user_id)

# @chat_bp.route('/chat', methods=['GET', 'POST'])
# def chat():
#     user_id = int(session.get('user_id'))
#     print(f"user_id: {user_id}")
#     return render_template('header.html', user_id=user_id)

# @map_bp.route('/map', methods=['GET', 'POST'])
# def map():
#     user_id = int(session.get('user_id'))
#     print(f"user_id: {user_id}")
#     return render_template('header.html', user_id=user_id)

# @login_bp.route('/group', methods=['GET', 'POST'])
# def group():
#     user_id = int(session.get('user_id'))
#     print(f"user_id: {user_id}")
#     return render_template('header.html', user_id=user_id)

# @login_bp.route('/show_event', methods=['GET', 'POST'])
# def event():
#     user_id = int(session.get('user_id'))
#     print(f"user_id: {user_id}")
#     return render_template('header.html', user_id=user_id)

# @logout_bp.route('/logout', methods=['GET', 'POST'])
# def logout():
#     user_id = session.get('user_id')
        # print(f"user_id: {user_id}")
#     return render_template('header.html', user_id=user_id)