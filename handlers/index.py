from flask import Blueprint,render_template


index_blue=Blueprint('index',__name__)

@index_blue.route('/')
def index():
    return render_template('index.html')