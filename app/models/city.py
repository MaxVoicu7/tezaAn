from db.db_connect import db 

class City(db.Model):
  __tablename__ = 'city'

  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(20), nullable=False)
  region = db.Column(db.String(20), nullable=False)
  postal_code = db.Column(db.String(10), nullable=True)

  def __repr__(self):
    return f'<City {self.name}>'