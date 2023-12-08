from sqlalchemy import inspect
from db.db_connect import db
from flask import jsonify

def index():
  return 'Azi e o zi de succes 123456789'

def get_tables():
  try:
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    return jsonify(tables)
  except Exception as e:
    return jsonify({"error": str(e)}), 500