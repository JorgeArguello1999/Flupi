from flask import Blueprint, render_template
from flask import jsonify
from flask import redirect, url_for

import _database_

notify_bp = Blueprint('notify', __name__, url_prefix='/notify', template_folder='templates', static_folder='static')

# Notify Front
@notify_bp.route('/notify_f', methods=['GET'])
def notify_frontend():
    return render_template('notify.html')

# Notify Status
@notify_bp.route('/', methods=['GET'])
def notify_status():
    work = _database_.get_alarm_status()

    return jsonify({
        "status": work
    })

# Notify Back
@notify_bp.route("/<int:statuswork>", methods=["GET"])
def notify_backend(statuswork):
    """
    Parámetros:
        - statuswork (int): 1 para llamar al técnico, 0 para desactivar.
    Retorna: Redirección a la página 'notify_f'.
    """
    _database_.update_alarm_status(statuswork)
    return redirect(url_for('notify.notify_frontend'))