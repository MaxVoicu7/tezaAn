from models.discount_instance import DiscountInstance
from db.db_connect import db

def fetch_discount_instances(discount_id):
  
  """
    Retrieves all discount instances for a specific discount.
    
    Args:
      discount_id: The ID of the discount.
    
    Returns:
      A list of DiscountInstance instances.
  """
  
  return DiscountInstance.query.filter_by(discount_id=discount_id).all()



def delete_discount_instance_by_id(discount_id):
  
  """
    Deletes all the discount instances with ID
    
    Args:
      discount_id: The ID of the discount.
  """

  DiscountInstance.query.filter_by(discount_id=discount_id).delete()




def add_discount_instances(discount_id, store_ids):
  
  """
    Adds discount instances for each store ID.

    Args:
      discount_id: The ID of the discount.
      store_ids: List of store IDs.
  """
  for store_id in store_ids:
    new_instance = DiscountInstance(discount_id=discount_id, store_id=store_id)
    db.session.add(new_instance)