from flask import Blueprint
from controllers.controller import get_categories, get_discounts, process_request
from controllers.product import get_products, add_product
from controllers.manufacturer import get_manufacturers
from controllers.admin_discount import get_expired_discounts, get_actual_discounts, get_future_discounts, get_discount_counts
from controllers.store import get_stores_in_network_one

main_blueprint = Blueprint('main', __name__)

main_blueprint.route('/category', methods=['GET'])(get_categories)

main_blueprint.route('/discount', methods=['GET'])(get_discounts)

main_blueprint.route('/discount-info', methods=['POST'])(process_request)

main_blueprint.route('/product', methods=['GET'])(get_products)
main_blueprint.route('/product', methods=['POST'])(add_product)

main_blueprint.route('/manufacturer', methods=['GET'])(get_manufacturers)

main_blueprint.route('/admin-expired-discount', methods=['GET'])(get_expired_discounts)
main_blueprint.route('/admin-actual-discount', methods=['GET'])(get_actual_discounts)
main_blueprint.route('/admin-future-discount', methods=['GET'])(get_future_discounts)

main_blueprint.route('/admin-discount', methods=['GET'])(get_discount_counts)

main_blueprint.route('/store', methods=['GET'])(get_stores_in_network_one)