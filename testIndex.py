from flask import Blueprint
from flask import render_template
testIndex_bp = Blueprint('testIndex',__name__)

@testIndex_bp.route("/testIndex")
def index():
    return render_template("testIndex.html")