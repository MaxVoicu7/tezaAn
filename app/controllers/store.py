from flask import jsonify
from db.db_connect import db
from models.store import Store
from models.city import City

def get_stores_in_network_one():
    try:
        # Obține toate unitățile cu network_id egal cu 1 și include orașul
        stores = db.session.query(
            Store, City.name.label("city_name")
        ).join(
            City, Store.city_id == City.id
        ).filter(
            Store.network_id == 1
        ).all()

        # Crează o listă de dicționare cu informațiile despre magazine
        stores_list = [{
            'store_id': store.Store.id,
            'store_name': store.Store.name,
            'city_name': store.city_name,  # Numele orașului
            'address': store.Store.address,
            'opening_hour': store.Store.opening_hour.strftime("%H:%M") if store.Store.opening_hour else None,
            'closing_hour': store.Store.closing_hour.strftime("%H:%M") if store.Store.closing_hour else None,
            'is_open_24_7': store.Store.is_open_24_7
            # Poți adăuga alte informații necesare
        } for store in stores]

        return jsonify(stores_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500