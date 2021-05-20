from flask import Blueprint

bp_it = Blueprint('it', __name__)

from app.items import view
