from sqlalchemy import inspect
from db.db_connect import db
from flask import jsonify
from models.product_category import ProductCategory
from models.discount import Discount
from models.complementary_discount import ComplementaryDiscount
from models.fixed_value_discount import FixedValueDiscount
from models.quantity_discount import QuantityDiscount
from models.percentage_discount import PercentageDiscount
from models.product import Product

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
                'discount_type_id': discount.discount_type_id, 
                'start_date': discount.start_date.isoformat(),
                'end_date': discount.end_date.isoformat()
            }

            # Adaugă informații specifice în funcție de discount_type_id
            if discount.discount_type_id == 1:  # Percentage Discount
                details = PercentageDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == PercentageDiscount.product_id).first()
                if details:
                    discount_data['percentage'] = details.discount_percentage
                    discount_data['initial_price'] = str(details.product.price)
                    discount_data['final_price'] = str(details.final_price)
            elif discount.discount_type_id == 2:  # Fixed Value Discount
                details = FixedValueDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == FixedValueDiscount.product_id).first()
                if details:
                    discount_data['discount_amount'] = str(details.discount_amount)
                    discount_data['initial_price'] = str(details.product.price)
                    discount_data['final_price'] = str(details.final_price)
            elif discount.discount_type_id == 3:  # Complementary Discount
                details = ComplementaryDiscount.query.filter_by(discount_id=discount.id).first()
                if details:
                    discount_data['offer_product_count'] = details.offer_product_count
                    discount_data['initial_price'] = str(details.initial_price)
                    discount_data['final_price'] = str(details.final_price)
            elif discount.discount_type_id == 4:  # Quantity Discount
                details = QuantityDiscount.query.filter_by(discount_id=discount.id).join(Product, Product.id == QuantityDiscount.product_id).first()
                if details:
                    discount_data['required_quantity'] = details.required_quantity
                    discount_data['free_quantity'] = details.free_quantity
                    discount_data['initial_price'] = str(details.product.price)
                    discount_data['final_price'] = str(details.final_price)

            discounts_list.append(discount_data)

        return jsonify(discounts_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

