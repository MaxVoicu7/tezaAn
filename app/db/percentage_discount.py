from db.db_connect import db
from models.product import Product
from models.percentage_discount import PercentageDiscount


def fetch_percentage_discount_details(discount_id):
  details = PercentageDiscount.query.filter_by(discount_id=discount_id).join(Product, Product.id == PercentageDiscount.product_id).first()
  
  if details:
    return {
      'discount_value': f"Reducere de {details.discount_percentage}%",
      'initial_price': str(details.product.price),
      'final_price': str(details.final_price),
      'product_name': details.product.name,
      'category_ids': details.product.category_id
    }
  
  return {}



def delete_percentage_discount(discount_id):
  
  """
    Deletes a percentage discount by its ID.

    Args:
      discount_id: The ID of the percentage discount to delete.
  """
  
  PercentageDiscount.query.filter_by(discount_id=discount_id).delete()




def create_percentage_discount(discount_id, product, discount_data):
  
  """
    Creates a new percentage discount.
    
    Args:
      discount_id: The ID of the newly created discount.
      product: The product associated with the discount.
      discount_data: Data containing discount details.
  """

  discount_percentage = int(discount_data['discount_percentage'])
  final_price = product.price - (product.price * discount_percentage / 100)

  new_percentage_discount = PercentageDiscount(
    discount_id=discount_id,
    product_id=product.id,
    discount_percentage=discount_percentage,
    final_price=final_price
  )
  
  db.session.add(new_percentage_discount)