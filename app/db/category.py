from models.product_category import ProductCategory





def fetch_all_categories():

  """
    Retrieves all product categories from the database.
    
    Returns:
      A list of ProductCategory instances.
  """
  
  return ProductCategory.query.all()