from flask import Blueprint

assess_bp = Blueprint('assess', __name__, url_prefix='/assess')

from . import views