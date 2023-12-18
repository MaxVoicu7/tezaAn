from flask import jsonify
from models.manufacturer import Manufacturer

def get_manufacturers():
    try:
        manufacturers = Manufacturer.query.with_entities(Manufacturer.id, Manufacturer.name).all()
        manufacturers_list = [{'id': m.id, 'name': m.name} for m in manufacturers]
        return jsonify(manufacturers_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500