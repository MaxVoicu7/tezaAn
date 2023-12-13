from sqlalchemy import inspect
from db.db_connect import db
from flask import jsonify, request
from models.manufacturer import Manufacturer


def get_manufacturers():
    try:
        manufacturers = Manufacturer.query.with_entities(Manufacturer.id, Manufacturer.name).all()
        manufacturers_list = [{'id': m.id, 'name': m.name} for m in manufacturers]
        return jsonify(manufacturers_list)
    except Exception as e:
        # În caz de eroare, returnează un mesaj de eroare ca răspuns JSON
        return jsonify({'error': str(e)}), 500