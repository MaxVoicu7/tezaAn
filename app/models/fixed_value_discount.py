from db.db_connect import db
from models.product import Product
from models.discount import Discount

class FixedValueDiscount(db.Model):
  __tablename__ = 'fixed_value_discount'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
  discount_amount = db.Column(db.Numeric(10, 2), nullable=False)
  final_price = db.Column(db.Numeric(10, 2), nullable=False)

  discount = db.relationship('Discount')
  product = db.relationship('Product')

  def __repr__(self):
    return f'<FixedValueDiscount {self.id} - Amount: {self.discount_amount}>'
