from db.db_connect import db
from models.city import City
from models.store import Store

def fetch_stores_by_network(network_id=1):

  """
    Retrieves all stores from the database for a given network.

    Args:
      network_id: The ID of the network to filter stores. Defaults to 1 for current testing purposes.

    Returns:
      A list of tuples containing Store and related City information.
  """
    
  return db.session.query( Store, City.name.label("city_name")
                  ).join( City, Store.city_id == City.id
                  ).filter( Store.network_id == network_id
                  ).all()
