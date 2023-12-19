from flask import jsonify
from db.manufacturer import fetch_all_manufacturers
from utils.transform import format_manufacturers_data

def get_manufacturers():
    
  """
    Controller function to get all manufacturers.
    Fetches manufacturer data from the database and formats them for a JSON response.
    
    Returns:
      A JSON response containing a list of manufacturers or an error message.
  """

  try:
    manufacturers = fetch_all_manufacturers()
    manufacturers_list = format_manufacturers_data(manufacturers)
    return jsonify(manufacturers_list)
  
  except Exception as e:
    return jsonify({'error': str(e)}), 500