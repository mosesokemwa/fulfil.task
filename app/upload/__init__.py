from flask import Blueprint

bp = Blueprint('uploads', __name__)

from app.upload import routes