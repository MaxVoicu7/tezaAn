from flask import jsonify
from db.category import fetch_all_categories
from utils.transform import format_categories_data





def get_categories():

  """
    Controller function to get all product categories.
    Fetches categories from the database and formats them for a JSON response.

    Returns:
      A JSON response containing a list of categories or an error message.
  """
  
  try:
    categories = fetch_all_categories()
    categories_list = format_categories_data(categories)
    return jsonify(categories_list)
  
  except Exception as e:
    return jsonify({"error": str(e)}), 500