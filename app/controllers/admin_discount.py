from flask import jsonify, request
from models.discount import Discount
from datetime import date, datetime
from db.db_connect import db
from db.discount import fetch_expired_discounts, fetch_actual_discounts, fetch_future_discounts
from db.discount import count_current_discounts, count_future_discounts, count_past_discounts
from db.discount_instance import add_discount_instances
from db.percentage_discount import create_percentage_discount
from db.fixed_value_discount import create_fixed_value_discount
from db.complementary_discount import create_complementary_discount
from db.quantity_discount import create_quantity_discount
from db.product import fetch_product_by_code
from utils.transform import format_discounts_for_json




def get_expired_discounts():
  
  """
    Controller function to get all expired discounts.
    Fetches expired discounts from the database and formats them for a JSON response.

    Returns:
      A JSON response containing a list of expired discounts or an error message.
  """

  try:
    expired_discounts = fetch_expired_discounts()
    discounts_list = format_discounts_for_json(expired_discounts)
    return jsonify(discounts_list)
  
  except Exception as e:
    return jsonify({'error': str(e)}), 500
    


def get_actual_discounts():
  """
    Controller function to get all actual discounts.
    Fetches actual discounts from the database and formats them for a JSON response.

    Returns:
      A JSON response containing a list of actual discounts or an error message.
  """

  try:
    actual_discounts = fetch_actual_discounts()
    discounts_list = format_discounts_for_json(actual_discounts)
    return jsonify(discounts_list)
  
  except Exception as e:
    return jsonify({'error': str(e)}), 500
    


def get_future_discounts():
  """
    Controller function to get all future discounts.
    Fetches future discounts from the database and formats them for a JSON response.

    Returns:
      A JSON response containing a list of future discounts or an error message.
  """

  try:
    future_discounts = fetch_future_discounts()
    discounts_list = format_discounts_for_json(future_discounts)
    return jsonify(discounts_list)
  
  except Exception as e:
    return jsonify({'error': str(e)}), 500
    


def get_discount_counts():
  
  """
    Controller function to get counts of current, past, and future discounts.

    Returns:
      A JSON response containing counts of different types of discounts.
  """
  
  try:
    today = date.today()

    current_discounts_count = count_current_discounts(today)
    past_discounts_count = count_past_discounts(today)
    future_discounts_count = count_future_discounts(today)

    return jsonify({
      "current_discounts_count": current_discounts_count,
      "past_discounts_count": past_discounts_count,
      "future_discounts_count": future_discounts_count
    })
  
  except Exception as e:
    return jsonify({'error': str(e)}), 500
    


def add_discount():
  discount_data = request.get_json()
  discount_type = int(discount_data['discount_type'])

  try:
    new_discount = Discount(
      description=discount_data['discount_description'],
      discount_type_id=int(discount_data['discount_type']),
      start_date=datetime.strptime(discount_data['start_date'], '%Y-%m-%d'),
      end_date=datetime.strptime(discount_data['end_date'], '%Y-%m-%d')
    )

    db.session.add(new_discount)
    db.session.flush()

    add_discount_instances(new_discount.id, discount_data['stores'])
        
    if discount_type == 1:
      product = fetch_product_by_code(discount_data['product_code'])
      create_percentage_discount(new_discount.id, product, discount_data)
    elif discount_type == 2:
      product = fetch_product_by_code(discount_data['product_code'])
      create_fixed_value_discount(new_discount.id, product, discount_data)
    elif discount_type == 3:
      create_complementary_discount(new_discount.id, discount_data)
    elif discount_type == 4:
      create_quantity_discount(new_discount.id, discount_data)

    db.session.commit()    
    return jsonify({"message": "Reducere primită și procesată cu succes!"}), 200
  
  except Exception as e:
    return jsonify({"error": str(e)}), 500