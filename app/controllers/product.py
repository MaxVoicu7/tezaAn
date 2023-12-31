from db.db_connect import db
from flask import jsonify, request

from db.product import fetch_products_with_details, create_product_instance, add_product_to_db
from utils.transform import format_product_data





def get_products():
  
  """
    Controller function to get product details.
    
    Returns:
      A JSON response containing a list of products with their details.
  """

  try:
    products = fetch_products_with_details()
    products_list = format_product_data(products)
    return jsonify(products_list)
  
  except Exception as e:
    return jsonify({"error": str(e)}), 500
    




def add_product():
  
  """
    Controller function to add a new product.
    Extracts product data from the request, creates a Product instance, and saves it to the database.
    
    Returns:
      A JSON response indicating the result of the operation.
  """

  product_data = request.get_json()

  try:
    new_product = create_product_instance(product_data)
    add_product_to_db(new_product)
    return jsonify({"message": "Produs adăugat cu succes!"}), 200
          
  except Exception as e:
    db.session.rollback()
    return jsonify({"error": str(e)}), 500