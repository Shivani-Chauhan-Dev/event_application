from flask import Blueprint 

bp = Blueprint("vendor" , __name__)

# from app.customer import routes
from . import routes