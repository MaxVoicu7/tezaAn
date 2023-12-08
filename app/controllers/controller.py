from sqlalchemy import inspect
from db.db_connect import db
from flask import jsonify

def index():
  return 'Azi e o zi de succes 123456789'

def get_tables():
  try:
    inspector = inspect(db.engine)
    columns = inspector.get_columns('city')
    column_info = [{'name': col['name'], 'type': str(col['type'])} for col in columns]
    return jsonify(column_info)
  except Exception as e:
    return jsonify({"error": str(e)}), 500