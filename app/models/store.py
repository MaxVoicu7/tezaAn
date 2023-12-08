# models/store.py
from db.db_connect import db
from models.city import City
from models.contact_info import ContactInfo
from models.store_network import StoreNetwork

class Store(db.Model):
  __tablename__ = 'store'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False)
  network_id = db.Column(db.Integer, db.ForeignKey('store_network.id'), nullable=False)
  address = db.Column(db.String(100))
  contact_id = db.Column(db.Integer, db.ForeignKey('contact_info.id'), nullable=False)
  opening_hour = db.Column(db.Time)
  closing_hour = db.Column(db.Time)
  is_open_24_7 = db.Column(db.Boolean, nullable=False)
  city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)

  city = db.relationship('City')
  network = db.relationship('StoreNetwork')
  contact_info = db.relationship('ContactInfo')

  def __repr__(self):
    return f'<Store {self.name}>'
