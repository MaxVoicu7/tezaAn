from db.db_connect import db
from models.contact_info import ContactInfo

class Manufacturer(db.Model):
  __tablename__ = 'manufacturer'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(40), nullable=False)
  contact_id = db.Column(db.Integer, db.ForeignKey('contact_info.id'), nullable=False)

  contact_info = db.relationship('ContactInfo')

  def __repr__(self):
    return f'<Manufacturer {self.name}>'