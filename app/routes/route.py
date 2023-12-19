from flask import Blueprint

# Importing controllers
from controllers.category import get_categories
from controllers.manufacturer import get_manufacturers
from controllers.store import get_stores_in_network_one
from controllers.product import get_products, add_product
from controllers.discount import get_discounts, get_discounts_by_params, update_discount, delete_discount, get_discount
from controllers.admin_discount import get_expired_discounts, get_actual_discounts, get_future_discounts, get_discount_counts, add_discount

# Creating a Blueprint for the main routes
main_blueprint = Blueprint('main', __name__)

main_blueprint.route('/category', methods=['GET'])(get_categories)

main_blueprint.route('/manufacturer', methods=['GET'])(get_manufacturers)

main_blueprint.route('/store', methods=['GET'])(get_stores_in_network_one)

main_blueprint.route('/product', methods=['GET'])(get_products)
main_blueprint.route('/product', methods=['POST'])(add_product)

main_blueprint.route('/discount', methods=['GET'])(get_discounts)
main_blueprint.route('/discount', methods=['POST'])(get_discounts_by_params)
main_blueprint.route('/discount/<int:discount_id>', methods=['GET'])(get_discount)
main_blueprint.route('/discount/<int:discount_id>', methods=['PUT'])(update_discount)
main_blueprint.route('/discount/<int:discount_id>', methods=['DELETE'])(delete_discount)

main_blueprint.route('/admin-discount', methods=['GET'])(get_discount_counts)
main_blueprint.route('/admin-discount', methods=['POST'])(add_discount)
main_blueprint.route('/admin-discount/expired', methods=['GET'])(get_expired_discounts)
main_blueprint.route('/admin-discount/actual', methods=['GET'])(get_actual_discounts)
main_blueprint.route('/admin-discount/future', methods=['GET'])(get_future_discounts)