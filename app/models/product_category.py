from db.db_connect import db

class ProductCategory(db.Model):
  __tablename__ = 'product_category'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100), nullable=False)

  def __repr__(self):
    return f'<ProductCategory {self.name}>'