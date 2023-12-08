from db.db_connect import db
from models.discount import Discount

class ComplementaryDiscount(db.Model):
  __tablename__ = 'complementary_discount'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  discount_id = db.Column(db.Integer, db.ForeignKey('discount.id'), nullable=False)
  offer_product_count = db.Column(db.Integer, nullable=False)
  initial_price = db.Column(db.Numeric(10, 2), nullable=False)
  final_price = db.Column(db.Numeric(10, 2), nullable=False)

  discount = db.relationship('Discount')

  def __repr__(self):
    return f'<ComplementaryDiscount {self.id}>'