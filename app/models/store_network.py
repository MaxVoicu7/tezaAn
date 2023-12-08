from db.db_connect import db
from models.contact_info import ContactInfo

class StoreNetwork(db.Model):
  __tablename__ = 'store_network'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(20), nullable=False)
  store_count = db.Column(db.Integer, nullable=True)
  contact_id = db.Column(db.Integer, db.ForeignKey('contact_info.id'), nullable=False)
  headquarters_address = db.Column(db.String(100), nullable=True)

  contact_info = db.relationship('ContactInfo')

  def __repr__(self):
    return f'<StoreNetwork {self.name}>'