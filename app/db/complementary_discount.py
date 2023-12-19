from db.db_connect import db
from db.product import fetch_product_by_code
from models.complementary_discount import ComplementaryDiscount
from models.complementary_discount_product import ComplementaryDiscountProduct
from models.product import Product


def fetch_complementary_discount_details(discount_id):
  details = ComplementaryDiscount.query.filter_by(discount_id=discount_id).first()
  
  if details:
    linked_products = ComplementaryDiscountProduct.query.filter_by(complementary_discount_id=details.id).join(Product, ComplementaryDiscountProduct.product_id == Product.id).all()
    product_names = [prod.product.name for prod in linked_products]
    categories = [prod.product.category_id for prod in linked_products]
    return {
      'discount_value': f"Cumpără {details.offer_product_count} produse și primește o reducere",
      'initial_price': str(details.initial_price),
      'final_price': str(details.final_price),
      'product_names': product_names,
      'category': categories
    }
  
  return {}


def delete_complementary_discount(discount_id):
  
  """
    Deletes a complementary discount by its ID, including related products.

    Args:
      discount_id: The ID of the complementary discount to delete.
  """
    
  comp_discounts = ComplementaryDiscount.query.filter_by(discount_id=discount_id).all()
  
  for cd in comp_discounts:
    ComplementaryDiscountProduct.query.filter_by(complementary_discount_id=cd.id).delete()
  
  ComplementaryDiscount.query.filter_by(discount_id=discount_id).delete()




def create_complementary_discount(discount_id, discount_data):
  
  """
    Creates a new complementary discount.

    Args:
      discount_id: The ID of the newly created discount.
      discount_data: Data containing discount details.
  """
  
  product_codes = discount_data['product_codes']
  final_price = float(discount_data['final_price'])

  initial_price = 0
  product_ids = []
  
  for code in product_codes:
    product = fetch_product_by_code(code)
    initial_price += float(product.price)
    product_ids.append(product.id)

  new_complementary_discount = ComplementaryDiscount(
    discount_id=discount_id,
    offer_product_count=len(product_codes),
    initial_price=initial_price,
    final_price=final_price
  )

  db.session.add(new_complementary_discount)
  db.session.flush()

  for product_id in product_ids:
    new_complementary_discount_product = ComplementaryDiscountProduct(
      complementary_discount_id=new_complementary_discount.id,
      product_id=product_id
    )

    db.session.add(new_complementary_discount_product)