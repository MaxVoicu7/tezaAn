from db.db_connect import db
from models.product_category import ProductCategory
from models.contact_info import ContactInfo

class Product(db.Model):
  __tablename__ = 'product'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(50), nullable=False)
  volume = db.Column(db.Numeric(10, 2))
  manufacturer_id = db.Column(db.Integer, db.ForeignKey('manufacturer.id'), nullable=False)
  unique_code = db.Column(db.String(255), nullable=False, unique=True)
  price = db.Column(db.Numeric(10, 2), nullable=False)
  category_id = db.Column(db.Integer, db.ForeignKey('product_category.id'), nullable=False)

  manufacturer = db.relationship('Manufacturer')
  category = db.relationship('ProductCategory')

  def __repr__(self):
    return f'<Product {self.name}>'
