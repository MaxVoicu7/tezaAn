from flask import jsonify, request
from sqlalchemy import and_
from models.discount import Discount
from models.discount import DiscountType
from datetime import date

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