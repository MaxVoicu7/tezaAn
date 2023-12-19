from sqlalchemy import and_
from db.db_connect import db
from datetime import date, datetime
from models.discount import Discount
from models.discount_type import DiscountType
from db.percentage_discount import delete_percentage_discount
from db.fixed_value_discount import delete_fixed_value_discount
from db.quantity_discount import delete_quantity_discount
from db.complementary_discount import delete_complementary_discount
from db.discount_instance import delete_discount_instance_by_id

def fetch_discounts():
  
  """
    Retrieves all discounts from the database.
    
    Returns:
        A list of Discount instances.
  """
  
  today = datetime.now().date()
  return Discount.query.filter(Discount.end_date >= today).all()



def fetch_discount_by_id(discount_id):

  """
    Fetches a discount by its ID.
    
    Args:
      discount_id: The ID of the discount to fetch.

    Returns:
      The Discount object if found, otherwise None.
  """
  
  return Discount.query.get(discount_id)



def update_discount_details(discount, data):

  """
    Updates the details of a discount object with new data.

    Args:
        discount: The Discount object to be updated.
        data: A dictionary containing the new discount data.
  """

  discount.description = data.get('discount_description', discount.description)
  discount.start_date = data.get('start_date', discount.start_date)
  discount.end_date = data.get('end_date', discount.end_date)



def delete_discount_entities(discount_id):
  
  """
    Deletes the main discount entity, associated discount instances, and specific type details.

    Args:
        discount_id: The ID of the discount to delete.
  """

  delete_discount_instance_by_id(discount_id)
  discount = Discount.query.get_or_404(discount_id)

  if discount.discount_type_id == 1:
    delete_percentage_discount(discount_id)
  elif discount.discount_type_id == 2:
    delete_fixed_value_discount(discount_id)
  elif discount.discount_type_id == 3:
    delete_complementary_discount(discount_id)
  elif discount.discount_type_id == 4:
    delete_quantity_discount(discount_id)

  db.session.delete(discount)
  db.session.commit()



def fetch_expired_discounts():
  
  """
    Fetches discounts that have expired as of today.

    Returns:
      A list of expired Discount objects.
  """
  
  return Discount.query.join(DiscountType, Discount.discount_type_id == DiscountType.id
                      ).filter(Discount.end_date < date.today()
                      ).all()



def fetch_actual_discounts():
  
  """
    Fetches discounts that are actual as of today.

    Returns:
      A list of actual Discount objects.
  """
  
  return Discount.query.join(DiscountType, Discount.discount_type_id == DiscountType.id
                      ).filter(and_(Discount.start_date <= date.today(), Discount.end_date >= date.today())
                      ).all()



def fetch_future_discounts():
  
  """
    Fetches discounts that will take place in the future as of today.

    Returns:
      A list of future Discount objects.
  """
  
  return Discount.query.join(DiscountType, Discount.discount_type_id == DiscountType.id
                      ).filter(Discount.start_date > date.today()
                      ).all()



def count_current_discounts(today):

  """
    Counts the number of discounts currently active.
    
    Args:
        today: The current date.

    Returns:
        The count of current discounts.
  """

  return Discount.query.filter( Discount.start_date <= today, Discount.end_date >= today
                      ).count()



def count_past_discounts(today):

  """
    Counts the number of discounts that have ended.
    
    Args:
      today: The current date.

    Returns:
      The count of past discounts.
  """
  
  return Discount.query.filter(Discount.end_date < today
                      ).count()



def count_future_discounts(today):

  """
    Counts the number of discounts that will start in the future.
    
    Args:
        today: The current date.

    Returns:
        The count of future discounts.
  """

  return Discount.query.filter(Discount.start_date > today
                      ).count()




