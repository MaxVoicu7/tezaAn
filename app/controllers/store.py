from flask import jsonify
from db.store import fetch_stores_by_network
from utils.transform import format_stores_data

def get_stores_in_network_one():
    
  """
    Controller function to get all stores in a specific network (currently network one).
    Fetches stores from the database and formats them for a JSON response.
    
    Returns:
      A JSON response containing a list of stores or an error message.
  """
  
  try:
    stores = fetch_stores_by_network()
    stores_list = format_stores_data(stores)
    return jsonify(stores_list)
  
  except Exception as e:
    return jsonify({'error': str(e)}), 500