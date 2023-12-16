from sqlalchemy import inspect
from db.db_connect import db
from flask import jsonify, request
from models.product_category import ProductCategory
from models.discount import Discount
from models.discount_instance import DiscountInstance
from models.complementary_discount import ComplementaryDiscount
from models.fixed_value_discount import FixedValueDiscount
from models.quantity_discount import QuantityDiscount
from models.percentage_discount import PercentageDiscount
from models.product import Product
from models.complementary_discount_product import ComplementaryDiscountProduct



def get_categories():
  try:
    categories = ProductCategory.query.all()
    categories_list = [{'id': category.id, 'name': category.name} for category in categories]
    return jsonify(categories_list)
  except Exception as e:
    return jsonify({"error": str(e)}), 500
  


def get_discounts():
  try:
    discounts = Discount.query.all()
      
    discounts_list = []
    for discount in discounts:
      discount_data = {
        'id': discount.id, 
        'description': discount.description, 
        'start_date': discount.start_date.isoformat(),
        'end_date': discount.end_date.isoformat(),
        'products': [],
        'discount_value': None,
        'initial_price': None,
        'final_price': None
			}

      discount_instances = DiscountInstance.query.filter_by(discount_id=discount.id).all()

      stores = []
      for instance in discount_instances:
        store = instance.store
        store_data = {
            'name': store.name,
            'address': store.address,
            'working_hours': '24/7' if store.is_open_24_7 else f'{store.opening_hour.strftime("%H:%M")} - {store.closing_hour.strftime("%H:%M")}'
        }
        stores.append(store_data)

    
      discount_data['stores'] = stores
      
      if discount.discount_type_id == 1:
        details = PercentageDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == PercentageDiscount.product_id).first()
        
        if details:
          discount_data['discount_value'] = f"Reducere de {details.discount_percentage}%"
          discount_data['initial_price'] = str(details.product.price)
          discount_data['final_price'] = str(details.final_price)
          discount_data['products'].append(details.product.name)

      elif discount.discount_type_id == 2:
        details = FixedValueDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == FixedValueDiscount.product_id).first()
        
        if details:
          discount_data['discount_value'] = f"Reducere de {details.discount_amount} lei"
          discount_data['initial_price'] = str(details.product.price)
          discount_data['final_price'] = str(details.final_price)
          discount_data['products'].append(details.product.name)

      elif discount.discount_type_id == 3:
        details = ComplementaryDiscount.query.filter_by(discount_id=discount.id).first()
        
        if details:
          discount_data['discount_value'] = f"Cumpără {details.offer_product_count} produse și primește o reducere"
          discount_data['initial_price'] = str(details.initial_price)
          discount_data['final_price'] = str(details.final_price)

          linked_products = ComplementaryDiscountProduct.query.filter_by(complementary_discount_id=details.id).join(Product, ComplementaryDiscountProduct.product_id == Product.id).all()
          for prod in linked_products:
            discount_data['products'].append(prod.product.name)

      elif discount.discount_type_id == 4:
        details = QuantityDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == QuantityDiscount.product_id).first()
        
        if details:
          discount_data['discount_value'] = f"Cumpără {details.required_quantity} produse și primește {details.free_quantity} gratis"
          discount_data['initial_price'] = str(details.product.price * (details.required_quantity + details.free_quantity))
          discount_data['final_price'] = str(details.final_price)
          discount_data['products'].append(details.product.name)

      discounts_list.append(discount_data)	

    return jsonify(discounts_list)
  except Exception as e:
        return jsonify({"error": str(e)}), 500	
  



def process_request():
  data = request.json
  category_id = int(data['category'])
  price_range = data['priceRange']
  start_price = float(price_range['start'])
  end_price = float(price_range['end'])

  discounts = Discount.query.all()
      
  discounts_list = []
  for discount in discounts:
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

      discount_instances = DiscountInstance.query.filter_by(discount_id=discount.id).all()

      stores = []
      for instance in discount_instances:
        store = instance.store
        store_data = {
            'name': store.name,
            'address': store.address,
            'working_hours': '24/7' if store.is_open_24_7 else f'{store.opening_hour.strftime("%H:%M")} - {store.closing_hour.strftime("%H:%M")}'
        }
        stores.append(store_data)

    
      discount_data['stores'] = stores
      
      if discount.discount_type_id == 1:
        details = PercentageDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == PercentageDiscount.product_id).first()
        
        if details:
          discount_data['discount_value'] = f"Reducere de {details.discount_percentage}%"
          discount_data['initial_price'] = str(details.product.price)
          discount_data['final_price'] = str(details.final_price)
          discount_data['products'].append(details.product.name)
          discount_data['category_id'].append(details.product.category_id)

      elif discount.discount_type_id == 2:
        details = FixedValueDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == FixedValueDiscount.product_id).first()
        
        if details:
          discount_data['discount_value'] = f"Reducere de {details.discount_amount} lei"
          discount_data['initial_price'] = str(details.product.price)
          discount_data['final_price'] = str(details.final_price)
          discount_data['products'].append(details.product.name)
          discount_data['category_id'].append(details.product.category_id)

      elif discount.discount_type_id == 3:
        details = ComplementaryDiscount.query.filter_by(discount_id=discount.id).first()
        
        if details:
          discount_data['discount_value'] = f"Cumpără {details.offer_product_count} produse și primește o reducere"
          discount_data['initial_price'] = str(details.initial_price)
          discount_data['final_price'] = str(details.final_price)

          linked_products = ComplementaryDiscountProduct.query.filter_by(complementary_discount_id=details.id).join(Product, ComplementaryDiscountProduct.product_id == Product.id).all()
          for prod in linked_products:
            discount_data['products'].append(prod.product.name)
            discount_data['category_id'].append(prod.product.category_id)


      elif discount.discount_type_id == 4:
        details = QuantityDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == QuantityDiscount.product_id).first()
        
        if details:
          discount_data['discount_value'] = f"Cumpără {details.required_quantity} produse și primește {details.free_quantity} gratis"
          discount_data['initial_price'] = str(details.product.price * (details.required_quantity + details.free_quantity))
          discount_data['final_price'] = str(details.final_price)
          discount_data['products'].append(details.product.name)
          discount_data['category_id'].append(details.product.category_id)

      discounts_list.append(discount_data)

  filtered_discounts = []


  for discount in discounts_list:
    # Verifică dacă category_id este 0 sau dacă este în lista de categorii
    is_category_matched = category_id == 0 or category_id in discount['category_id']

    # Verifică dacă prețul final se încadrează în intervalul dorit
    is_price_matched = float(discount['final_price']) >= start_price and float(discount['final_price']) <= end_price

    # Adaugă reducerea în lista filtrată doar dacă ambele condiții (categorie și preț) sunt îndeplinite
    if is_category_matched and is_price_matched:
        filtered_discounts.append(discount)
  
  return jsonify(filtered_discounts)