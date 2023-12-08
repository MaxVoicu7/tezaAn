from db.db_connect import db
from models.store import Store
from models.discount import Discount

class DiscountInstance(db.Model):
  __tablename__ = 'discount_instance'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'), nullable=False)
  store_id = db.Column(db.Integer, db.ForeignKey('store.id'), nullable=False)

  discount = db.relationship('Discount')
  store = db.relationship('Store')

  def __repr__(self):
    return f'<DiscountInstance {self.id}>'