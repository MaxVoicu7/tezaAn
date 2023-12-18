from sqlalchemy import inspect
from db.db_connect import db
from flask import jsonify, request
from models.product import Product
from models.product_category import ProductCategory
from models.manufacturer import Manufacturer

def get_products():
    try:
        products = db.session.query(
            Product, Manufacturer, ProductCategory
        ).join(
            Manufacturer, Product.manufacturer_id == Manufacturer.id
        ).join(
            ProductCategory, Product.category_id == ProductCategory.id
        ).all()

        # Convertirea listei de produse într-un format JSON
        products_list = [{
            'product_id': product.Product.id,
            'product_name': product.Product.name,
            'unique_code': product.Product.unique_code,
            'product_volume': str(product.Product.volume),
            'product_price': str(product.Product.price),
            'manufacturer_name': product.Manufacturer.name,
            'category_name': product.ProductCategory.name
        } for product in products]

        return jsonify(products_list)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    






def add_product():
    product_data = request.get_json()

    try:
        # Creează o nouă instanță a modelului Product
        new_product = Product(
            name=product_data['name'],
            volume=product_data['volume'],
            manufacturer_id=product_data['manufacturerId'],
            unique_code=product_data['uniqueCode'],
            price=product_data['price'],
            category_id=product_data['categoryId']
        )
        
        # Adaugă produsul nou în sesiunea bazei de date
        db.session.add(new_product)
        # Salvează modificările în baza de date
        db.session.commit()

        return jsonify({"message": "Produs adăugat cu succes!"}), 200
    except Exception as e:
        # Dacă ceva nu merge bine, anulează toate modificările făcute în sesiunea curentă
        db.session.rollback()
        return jsonify({"error": str(e)}), 500