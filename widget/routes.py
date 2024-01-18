from flask import Blueprint 
from flask import jsonify

from dotenv import load_dotenv
load_dotenv()

from databases import images

from chat.routes import chatbot_post

widget_bp = Blueprint('widget', __name__, url_prefix='/widget', template_folder='templates', static_folder='static')

@widget_bp.route('/', methods=['POST'])
def widget_post():
    return chatbot_post()

@widget_bp.route('photos/', methods=['GET'])
def widget_get():
    try:
        photo_chatbot = images.get_image('chatbot')
    except Exception as e:
        print("Error: ", e)
        photo_chatbot = ''
    
    try:
        photo_user = images.get_image('usuario')
    except Exception as e:
        print("Error: ", e)
        photo_user = ''
    
    return jsonify({
        "photo_user": photo_user,
        "photo_role": photo_chatbot
    })