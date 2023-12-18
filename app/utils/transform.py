


def transform_product_data(products):
  """
    Transforms product data into a list of dictionaries suitable for JSON response.

    Args:
      products: A list of tuples containing Product, Manufacturer, and ProductCategory objects.

    Returns:
      A list of dictionaries with product details.
  """
  
  return [{
    'product_id': product.Product.id,
    'product_name': product.Product.name,
    'unique_code': product.Product.unique_code,
    'product_volume': str(product.Product.volume),
    'product_price': str(product.Product.price),
    'manufacturer_name': product.Manufacturer.name,
    'category_name': product.ProductCategory.name
  } for product in products]