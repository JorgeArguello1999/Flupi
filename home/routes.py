from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__, url_prefix='/home')

# Home
@home_bp.route('/', methods=['GET'])
def home():
    return render_template('index.html')