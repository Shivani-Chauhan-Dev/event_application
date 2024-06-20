from flask import Blueprint 

bp = Blueprint("event" , __name__)

from . import routes
