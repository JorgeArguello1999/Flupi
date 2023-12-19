from flask import Blueprint, render_template

chat_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot', template_folder='templates', static_folder='static')

# Chatbot Front
@chat_bp.route('/', methods=['GET'])
def chatbot_get():
    return render_template('chatbot.html')
