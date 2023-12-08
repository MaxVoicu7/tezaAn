from db.db_connect import db
from models.complementary_discount import ComplementaryDiscount
from models.product import Product

class ComplementaryDiscountProduct(db.Model):
  __tablename__ = 'complementary_discount_product'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  complementary_discount_id = db.Column(db.Integer, db.ForeignKey('complementary_discount.id'), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)

  complementary_discount = db.relationship('ComplementaryDiscount')
  product = db.relationship('Product')

  def __repr__(self):
    return f'<ComplementaryDiscountProduct {self.id}>'
