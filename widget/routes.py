from flask import Blueprint 

from dotenv import load_dotenv
load_dotenv()

widget_bp = Blueprint('widget', __name__, url_prefix='/widget', template_folder='templates', static_folder='static')


