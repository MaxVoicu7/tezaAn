from db.db_connect import db
from models.product import Product
from models.product_category import ProductCategory
from models.manufacturer import Manufacturer


def fetch_products_with_details():

  """
    Fetches product data along with manufacturer and category details from the database.
    This function performs a join operation on the Product, Manufacturer, and ProductCategory tables.

    Returns:
      A list of tuples containing Product, Manufacturer, and ProductCategory objects, representing the combined data from these tables.
  """

  return db.session.query( Product, Manufacturer, ProductCategory
                  ).join( Manufacturer, Product.manufacturer_id == Manufacturer.id
                  ).join( ProductCategory, Product.category_id == ProductCategory.id
                  ).all()





def create_product_instance(product_data):

  """
    Creates a new instance of the Product model from provided data.

    Args:
      product_data: A dictionary containing product details.

    Returns:
      An instance of the Product model.
  """
  
  return Product(
    name=product_data['name'],
    volume=product_data['volume'],
    manufacturer_id=product_data['manufacturer_id'],
    unique_code=product_data['unique_code'],
    price=product_data['price'],
    category_id=product_data['category_id']
  )





def add_product_to_db(product):

  """
    Adds a new product to the database session and commits the transaction.

    Args:
      product: An instance of the Product model to be added to the database.
  """

  db.session.add(product)
  db.session.commit()





def fetch_product_by_code(product_code):
  
  """
    Fetches a product by its unique code.

    Args:
      product_code: Unique code of the product.

    Returns:
      The Product object if found, otherwise raises ValueError.
  """

  product = Product.query.filter_by(unique_code=product_code).first()
  if product is None:
    raise ValueError(f'Produsul cu codul {product_code} nu a fost găsit')
    
  return product