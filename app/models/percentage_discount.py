from db.db_connect import db
from models.discount import Discount
from models.product import Product

class PercentageDiscount(db.Model):
  __tablename__ = 'percentage_discount'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
  discount_percentage = db.Column(db.SmallInteger, nullable=False)
  final_price = db.Column(db.Numeric(10, 2), nullable=False)

  discount = db.relationship('Discount')
  product = db.relationship('Product')

  def __repr__(self):
    return f'<PercentageDiscount {self.id} - {self.discount_percentage}%>'
