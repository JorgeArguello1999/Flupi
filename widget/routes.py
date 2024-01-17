from flask import Blueprint 
from flask import request
from flask import jsonify

from dotenv import load_dotenv
load_dotenv()

from chat.routes import chatbot_post

widget_bp = Blueprint('widget', __name__, url_prefix='/widget', template_folder='templates', static_folder='static')

@widget_bp.route('/', methods=['POST'])
def widget_post():
    return chatbot_post()