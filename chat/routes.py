from flask import Blueprint, render_template

from databases import usuarios

chat_bp = Blueprint('chatbot', __name__, url_prefix='/chatbot', template_folder='templates', static_folder='static')

# Chatbot Front
@chat_bp.route('/', methods=['GET'])
def chatbot_get():
    try:
        chatbot = usuarios.get_user_by_username('chatbot')[1]
    except:
        chatbot = "No existe usuario"
    return render_template('chatbot.html', token=chatbot)
