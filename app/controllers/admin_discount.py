from flask import jsonify, request
from sqlalchemy import and_
from models.discount import Discount
from models.discount import DiscountType
from models.discount_instance import DiscountInstance
from models.percentage_discount import PercentageDiscount
from models.fixed_value_discount import FixedValueDiscount
from models.complementary_discount import ComplementaryDiscount
from models.complementary_discount_product import ComplementaryDiscountProduct
from models.quantity_discount import QuantityDiscount
from models.product import Product
from datetime import date, datetime
from db.db_connect import db

def get_expired_discounts():
    try:
        # Obține reducerile valabile până în ziua de azi
        valid_discounts = Discount.query.join(
            DiscountType, Discount.discount_type_id == DiscountType.id
        ).filter(
            Discount.end_date < date.today()
        ).all()

        # Crează o listă de dicționare cu informațiile despre reduceri
        discounts_list = [{
            'discount_id': discount.id,
            'discount_description': discount.description,
            'start_date': discount.start_date.isoformat(),
            'end_date': discount.end_date.isoformat(),
            'discount_type': discount.discount_type.name
        } for discount in valid_discounts]

        return jsonify(discounts_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


def get_actual_discounts():
    try:
        # Obține reducerile valabile până în ziua de azi
        valid_discounts = Discount.query.join(
            DiscountType, Discount.discount_type_id == DiscountType.id
        ).filter(
            and_(Discount.start_date <= date.today(), Discount.end_date >= date.today())
        ).all()

        # Crează o listă de dicționare cu informațiile despre reduceri
        discounts_list = [{
            'discount_id': discount.id,
            'discount_description': discount.description,
            'start_date': discount.start_date.isoformat(),
            'end_date': discount.end_date.isoformat(),
            'discount_type': discount.discount_type.name
        } for discount in valid_discounts]

        return jsonify(discounts_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

def get_future_discounts():
    try:
        # Obține reducerile valabile până în ziua de azi
        valid_discounts = Discount.query.join(
            DiscountType, Discount.discount_type_id == DiscountType.id
        ).filter(
            Discount.start_date > date.today()
        ).all()

        # Crează o listă de dicționare cu informațiile despre reduceri
        discounts_list = [{
            'discount_id': discount.id,
            'discount_description': discount.description,
            'start_date': discount.start_date.isoformat(),
            'end_date': discount.end_date.isoformat(),
            'discount_type': discount.discount_type.name
        } for discount in valid_discounts]

        return jsonify(discounts_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    


def get_discount_counts():
    try:
        today = date.today()

        # Numără reducerile actuale
        current_discounts_count = Discount.query.filter(
            Discount.start_date <= today, 
            Discount.end_date >= today
        ).count()

        # Numără reducerile anterioare
        past_discounts_count = Discount.query.filter(
            Discount.end_date < today
        ).count()

        # Numără reducerile viitoare
        future_discounts_count = Discount.query.filter(
            Discount.start_date > today
        ).count()

        return jsonify({
            "current_discounts_count": current_discounts_count,
            "past_discounts_count": past_discounts_count,
            "future_discounts_count": future_discounts_count
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    




def add_discount():
    discount_data = request.get_json()

    try:
        new_discount = Discount(
            description=discount_data['discount_description'],
            discount_type_id=int(discount_data['discount_type']),
            start_date=datetime.strptime(discount_data['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(discount_data['end_date'], '%Y-%m-%d')
        )

        db.session.add(new_discount)
        db.session.flush()

        store_ids = discount_data['stores']  # Array-ul cu ID-urile magazinelor
        for store_id in store_ids:
            new_discount_instance = DiscountInstance(discount_id=new_discount.id, store_id=store_id)
            db.session.add(new_discount_instance)

        
        if int(discount_data['discount_type']) == 1:
            product_code = int(discount_data['product_code'])
            discount_percentage = int(discount_data['discount_percentage'])

            # Căutarea produsului după product_code
            product = Product.query.filter_by(unique_code=product_code).first()
            if product is None:
                raise ValueError(f'Produsul cu codul {product_code} nu a fost găsit')

            # Calculul prețului final
            final_price = product.price - (product.price * discount_percentage / 100)

            new_percentage_discount = PercentageDiscount(
                discount_id=new_discount.id,
                product_id=product.id,
                discount_percentage=discount_percentage,
                final_price=final_price
            )
            db.session.add(new_percentage_discount)


        if int(discount_data['discount_type']) == 2:  # Presupunând că 2 reprezintă FixedValueDiscount
            product_code = int(discount_data['product_code'])
            discount_amount = float(discount_data['discount_fixed_value'])

            # Căutarea produsului după product_code
            product = Product.query.filter_by(unique_code=product_code).first()
            if product is None:
                raise ValueError(f'Produsul cu codul {product_code} nu a fost găsit')


            # Calculul prețului final
            final_price = max(float(product.price) - discount_amount, 0)  # Asigură-te că prețul final nu este negativ


            new_fixed_value_discount = FixedValueDiscount(
                discount_id=new_discount.id,
                product_id=product.id,
                discount_amount=discount_amount,
                final_price=final_price
            )
            db.session.add(new_fixed_value_discount)

        


        if int(discount_data['discount_type']) == 3:
            product_codes = discount_data['product_codes']
            final_price = float(discount_data['final_price'])

            initial_price = 0
            for code in product_codes:
                product = Product.query.filter_by(unique_code=code).first()
                if product is None:
                    raise ValueError(f'Produsul cu codul {code} nu a fost găsit')
                initial_price += float(product.price)

            new_complementary_discount = ComplementaryDiscount(
                discount_id=new_discount.id,
                offer_product_count=len(product_codes),
                initial_price=initial_price,
                final_price=final_price
            )
            db.session.add(new_complementary_discount)
            db.session.flush()

            for code in product_codes:
                product = Product.query.filter_by(unique_code=code).first()
                new_complementary_discount_product = ComplementaryDiscountProduct(
                    complementary_discount_id=new_complementary_discount.id,
                    product_id=product.id
                )
                db.session.add(new_complementary_discount_product)


        if int(discount_data['discount_type']) == 4:
            product_code = int(discount_data['product_code'])
            required_quantity = int(discount_data['required_quantity'])
            free_quantity = int(discount_data['free_quantity'])

            # Căutarea produsului după product_code
            product = Product.query.filter_by(unique_code=product_code).first()
            if product is None:
                raise ValueError(f'Produsul cu codul {product_code} nu a fost găsit')
            
            final_price = product.price * required_quantity

            new_quantity_discount = QuantityDiscount(
                discount_id=new_discount.id,
                product_id=product.id,
                required_quantity=required_quantity,
                free_quantity=free_quantity,
                final_price=final_price
            )
            db.session.add(new_quantity_discount)

        db.session.commit()
        

        return jsonify({"message": "Reducere primită și procesată cu succes!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    