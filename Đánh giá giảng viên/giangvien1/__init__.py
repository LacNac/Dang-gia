from flask import Blueprint

gv_bp = Blueprint('gv', __name__, url_prefix='/giang_vien')

from.import views