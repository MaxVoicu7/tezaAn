from models.manufacturer import Manufacturer

def fetch_all_manufacturers():
  
  """
    Retrieves all manufacturers from the database.
    
    Returns:
      A list of tuples containing manufacturer's id and name.
  """
  
  return Manufacturer.query.with_entities(Manufacturer.id, Manufacturer.name).all()