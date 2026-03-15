from flask import Blueprint

list_sb_bp = Blueprint('list_sb', __name__, url_prefix='/list_sb')

from . import views