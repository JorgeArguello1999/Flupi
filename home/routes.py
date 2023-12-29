from flask import Blueprint, render_template

from databases import home as content

home_bp = Blueprint('home', __name__, url_prefix='/home', template_folder='templates', static_folder='static')

# Home
@home_bp.route('/', methods=['GET'])
def home():
    html = content.get_home()
    return render_template('index.html', html=html)