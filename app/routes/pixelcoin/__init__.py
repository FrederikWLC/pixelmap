from flask import Blueprint
bp = Blueprint('erc360', __name__)

from app.routes.pixelcoin import routes