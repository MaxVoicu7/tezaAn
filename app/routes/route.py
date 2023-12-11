from flask import Blueprint
from controllers.controller import get_categories, get_discounts

main_blueprint = Blueprint('main', __name__)

main_blueprint.route('/category', methods=['GET'])(get_categories)
main_blueprint.route('/discount', methods=['GET'])(get_discounts)
