from flask import Blueprint
from controllers.controller import index, get_tables

main_blueprint = Blueprint('main', __name__)

main_blueprint.route('/', methods=['GET'])(index)
main_blueprint.route('/tables', methods=['GET'])(get_tables)