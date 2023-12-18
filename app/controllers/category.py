from flask import jsonify
from models.product_category import ProductCategory


def get_categories():

  """
    Fetches all product categories from the database and returns them in JSON format.

    Returns:
      A JSON response containing a list of product categories. Each category is represented as a dictionary with 'id' and 'name' keys.
      In case of an exception, returns a JSON response with an 'error' key and a 500 status code.
  """
  
  try:
    categories = ProductCategory.query.all()
    categories_list = [{'id': category.id, 'name': category.name} for category in categories]
    return jsonify(categories_list)
  except Exception as e:
    return jsonify({"error": str(e)}), 500