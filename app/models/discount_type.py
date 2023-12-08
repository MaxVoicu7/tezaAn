from db.db_connect import db

class DiscountType(db.Model):
  __tablename__ = 'discount_type'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(30), nullable=False)
  description = db.Column(db.String(255))
  table_name = db.Column(db.String(30), nullable=False)

  def __repr__(self):
    return f'<DiscountType {self.name}>'