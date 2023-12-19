from db.db_connect import db
from models.fixed_value_discount import FixedValueDiscount
from models.product import Product



def fetch_fixed_value_discount_details(discount_id):
  details = FixedValueDiscount.query.filter_by(discount_id=discount_id).join(Product, Product.id == FixedValueDiscount.product_id).first()
  
  if details:
    return {
      'discount_value': f"Reducere de {details.discount_amount} lei",
      'initial_price': str(details.product.price),
      'final_price': str(details.final_price),
      'product_name': details.product.name,
      'category_ids': details.product.category_id
    }
  
  return {}




def delete_fixed_value_discount(discount_id):
    
  """
    Deletes a fixed value discount by its ID.

    Args:
      discount_id: The ID of the fixed value discount to delete.
  """
  
  FixedValueDiscount.query.filter_by(discount_id=discount_id).delete()




def create_fixed_value_discount(discount_id, product, discount_data):
    
  """
    Creates a new fixed value discount.
    
    Args:
      discount_id: The ID of the newly created discount.
      product: The product associated with the discount.
      discount_data: Data containing discount details.
  """

  discount_amount = float(discount_data['discount_fixed_value'])
  final_price = max(float(product.price) - discount_amount, 0)

  new_fixed_value_discount = FixedValueDiscount(
    discount_id=discount_id,
    product_id=product.id,
    discount_amount=discount_amount,
    final_price=final_price
  )
  
  db.session.add(new_fixed_value_discount)