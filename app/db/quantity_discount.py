from db.db_connect import db
from db.product import fetch_product_by_code
from models.quantity_discount import QuantityDiscount
from models.product import Product


def fetch_quantity_discount_details(discount_id):
  details = QuantityDiscount.query.filter_by(discount_id=discount_id).join(Product, Product.id == QuantityDiscount.product_id).first()
  
  if details:
    return {
      'discount_value': f"Cumpără {details.required_quantity} produse și primește {details.free_quantity} gratis",
      'initial_price': str(details.product.price * (details.required_quantity + details.free_quantity)),
      'final_price': str(details.final_price),
      'product_name': details.product.name,
      'category_ids': details.product.category_id
    }
  
  return {}


def delete_quantity_discount(discount_id):
  
  """
    Deletes a quantity discount by its ID.

    Args:
      discount_id: The ID of the quantity discount to delete.
  """
  
  QuantityDiscount.query.filter_by(discount_id=discount_id).delete()



def create_quantity_discount(discount_id, discount_data):
  
  """
    Creates a new quantity discount.

    Args:
      discount_id: The ID of the newly created discount.
      discount_data: Data containing discount details.
  """

  product_code = int(discount_data['product_code'])
  required_quantity = int(discount_data['required_quantity'])
  free_quantity = int(discount_data['free_quantity'])

  product = fetch_product_by_code(product_code)
  final_price = product.price * required_quantity

  new_quantity_discount = QuantityDiscount(
    discount_id=discount_id,
    product_id=product.id,
    required_quantity=required_quantity,
    free_quantity=free_quantity,
    final_price=final_price
  )
  
  db.session.add(new_quantity_discount)