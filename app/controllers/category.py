from flask import jsonify
from models.product_category import ProductCategory


def get_categories():
  try:
    categories = ProductCategory.query.all()
    categories_list = [{'id': category.id, 'name': category.name} for category in categories]
    return jsonify(categories_list)
  except Exception as e:
    return jsonify({"error": str(e)}), 500