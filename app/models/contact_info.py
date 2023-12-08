from db.db_connect import db

class ContactInfo(db.Model):
  __tablename__ = 'contact_info'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  phone_number = db.Column(db.String(15), nullable=True)
  email = db.Column(db.String(50), nullable=True)

  def __repr__(self):
    return f'<ContactInfo {self.email}, {self.phone_number}>'