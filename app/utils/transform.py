def format_product_data(products):
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





def format_categories_data(categories):

  """
    Formats a list of category instances into a JSON-friendly list of dictionaries.

    Args:
      categories: A list of ProductCategory instances.

    Returns:
      A list of dictionaries, each representing a category.
  """
  
  return [{'id': category.id, 'name': category.name} for category in categories]





def format_manufacturers_data(manufacturers):

  """
    Formats a list of manufacturer tuples into a JSON-friendly list of dictionaries.

    Args:
      manufacturers: A list of tuples containing manufacturer's id and name.
    Returns:
      A list of dictionaries, each representing a manufacturer.
  """
  
  return [{'id': manufacturer.id, 'name': manufacturer.name} for manufacturer in manufacturers]





def format_stores_data(stores):
  
  """
    Formats a list of store tuples into a JSON-friendly list of dictionaries.

    Args:
        stores: A list of tuples containing Store and City information.

    Returns:
        A list of dictionaries, each representing a store.
  """
  
  return [{
    'store_id': store.Store.id,
    'store_name': store.Store.name,
    'city_name': store.city_name,
    'address': store.Store.address,
    'opening_hour': store.Store.opening_hour.strftime("%H:%M") if store.Store.opening_hour else None,
    'closing_hour': store.Store.closing_hour.strftime("%H:%M") if store.Store.closing_hour else None,
    'is_open_24_7': store.Store.is_open_24_7
  } for store in stores]





def format_store_info(store):
  
  """
    Formats store data for inclusion in the discount response.

    Args:
        store: A Store instance.

    Returns:
        A dictionary representing the store data.
  """

  working_hours = '24/7' if store.is_open_24_7 else f'{store.opening_hour.strftime("%H:%M")} - {store.closing_hour.strftime("%H:%M")}'
  
  return {
    'name': store.name,
    'address': store.address,
    'working_hours': working_hours
  }





def format_discounts_for_json(discounts):
  
  """
    Formats a list of discount objects into a JSON-friendly list of dictionaries.

    Args:
      discounts: A list of Discount objects.

    Returns:
      A list of dictionaries, each representing a discount.
  """

  return [{
    'discount_id': discount.id,
    'discount_description': discount.description,
    'start_date': discount.start_date.isoformat(),
    'end_date': discount.end_date.isoformat(),
    'discount_type': discount.discount_type.name
  } for discount in discounts]





def format_discount_data(discount, discount_details_func):
  discount_data = {
    'id': discount.id,
    'description': discount.description,
    'start_date': discount.start_date.isoformat(),
    'end_date': discount.end_date.isoformat(),
    'products': [],
    'discount_value': None,
    'initial_price': None,
    'final_price': None,
    'category_id': []
  }

  details = discount_details_func(discount.id)
  discount_data.update(details)

  if 'product_name' in details:
    discount_data['products'].append(details['product_name'])

  if 'product_names' in details:
    for product in details['product_names']:
      discount_data['products'].append(product)

  if 'category' in details:
    for category in details['category']:
      discount_data['category_id'].append(category)

  if 'category_ids' in details:
    discount_data['category_id'].append(details['category_ids'])

  return discount_data