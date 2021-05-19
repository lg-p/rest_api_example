from flask import Blueprint

bp_reg = Blueprint('reg', __name__)

from app.registration import view
