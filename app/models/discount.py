from db.db_connect import db
from datetime import date
from models.discount_type import DiscountType

class Discount(db.Model):
  __tablename__ = 'discount'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  description = db.Column(db.String(255), nullable=False)
  discount_type_id = db.Column(db.Integer, db.ForeignKey('discount_type.id'), nullable=False)
  start_date = db.Column(db.Date, nullable=False, default=date.today)
  end_date = db.Column(db.Date, nullable=False, default=date.today)

  discount_type = db.relationship('DiscountType')

  def __repr__(self):
    return f'<Discount {self.id} - {self.description}>'
