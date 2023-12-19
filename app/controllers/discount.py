from db.db_connect import db
from flask import jsonify, request
from db.discount import fetch_discounts, fetch_discount_by_id, update_discount_details, delete_discount_entities
from db.discount_instance import fetch_discount_instances
from db.percentage_discount import fetch_percentage_discount_details
from db.fixed_value_discount import fetch_fixed_value_discount_details
from db.complementary_discount import fetch_complementary_discount_details
from db.quantity_discount import fetch_quantity_discount_details
from utils.transform import format_store_info, format_discount_data



def get_discounts():
  try:
    discounts = fetch_discounts()
    discounts_list = []

    for discount in discounts:
      if discount.discount_type_id == 1:
        discount_data = format_discount_data(discount, fetch_percentage_discount_details)
      elif discount.discount_type_id == 2:
        discount_data = format_discount_data(discount, fetch_fixed_value_discount_details)
      elif discount.discount_type_id == 3:
        discount_data = format_discount_data(discount, fetch_complementary_discount_details)
      elif discount.discount_type_id == 4:
        discount_data = format_discount_data(discount, fetch_quantity_discount_details)

      discount_instances = fetch_discount_instances(discount.id)
      stores = [format_store_info(instance.store) for instance in discount_instances]
      discount_data['stores'] = stores

      discounts_list.append(discount_data)

    return jsonify(discounts_list)
  
  except Exception as e:
    return jsonify({"error": str(e)}), 500	
  


def get_discounts_by_params():
  data = request.json
  category_id = int(data['category'])
  price_range = data['priceRange']
  start_price = float(price_range['start'])
  end_price = float(price_range['end'])

  discounts = fetch_discounts()
  discounts_list = []
  
  for discount in discounts:
    if discount.discount_type_id == 1:
      discount_data = format_discount_data(discount, fetch_percentage_discount_details)
    elif discount.discount_type_id == 2:
      discount_data = format_discount_data(discount, fetch_fixed_value_discount_details)
    elif discount.discount_type_id == 3:
      discount_data = format_discount_data(discount, fetch_complementary_discount_details)
    elif discount.discount_type_id == 4:
      discount_data = format_discount_data(discount, fetch_quantity_discount_details)

    discount_instances = fetch_discount_instances(discount.id)
    stores = [format_store_info(instance.store) for instance in discount_instances]
    discount_data['stores'] = stores
      
    discounts_list.append(discount_data)

  filtered_discounts = []

  for discount in discounts_list:
    is_category_matched = category_id == 0 or category_id in discount['category_id']
    is_price_matched = float(discount['final_price']) >= start_price and float(discount['final_price']) <= end_price
    
    if is_category_matched and is_price_matched:
      filtered_discounts.append(discount)
  
  return jsonify(filtered_discounts)



def get_discount(discount_id):
  try:
    discount = fetch_discount_by_id(discount_id)

    if discount is None:
      raise ValueError(f"Discount with id {discount_id} not found.")
    
    discount_data = {
            "discount_id": discount.id,
            "discount_description": discount.description,
            "start_date": discount.start_date.strftime('%Y-%m-%d'),
            "end_date": discount.end_date.strftime('%Y-%m-%d'),
        }

    return jsonify({"success": True, "discount": discount_data}), 200

  except Exception as e:
    return jsonify({"success": False, "message": "A apărut o eroare"}), 500  



def update_discount(discount_id):

  """
    Updates a discount based on the provided ID and new data.

    Args:
      discount_id: The ID of the discount to be updated.

    Returns:
      A JSON response indicating the success or failure of the update operation.
  """

  try:
    discount_data = request.get_json()
    discount = fetch_discount_by_id(discount_id)

    if discount is None:
      raise ValueError(f"Discount with id {discount_id} not found.")

    update_discount_details(discount, discount_data)
    db.session.commit()

    return jsonify({"success": True, "message": "Datele au fost actualizate"}), 200

  except ValueError as ve:
    return jsonify({"success": False, "message": str(ve)}), 404
  
  except Exception as e:
    return jsonify({"success": False, "message": "A apărut o eroare la actualizarea datelor"}), 500
    


def delete_discount(discount_id):
    
  """
    Controller function to handle the deletion of a discount.

    Args:
      discount_id: The ID of the discount to be deleted.
    
    Returns:
      A JSON response indicating the success or failure of the operation.
  """
  
  try:
    delete_discount_entities(discount_id)
    return jsonify({"success": True, "message": "Reducerea a fost ștearsă."}), 200
  
  except Exception as e:
    return jsonify({"success": False, "message": "A apărut o eroare la ștergerea reducerii."}), 500