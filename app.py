from flask import Flask, request, jsonify
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import settings
from sqlalchemy.sql import func
from flask_restful import fields, marshal_with, marshal
from itertools import groupby
from datetime import datetime

"""
Creating flask application
"""
app = Flask(__name__)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code

for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)

"""
Configuring the flask application
"""

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = settings.SQLALCHEMY_TRACK_MODIFICATIONS
app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS

db = SQLAlchemy(app)
api = Api(app)
api.prefix = '/api'

from endpoints.customer_order_line.resource import CustomerOrderLineResource
from endpoints.customer_order_line.model import CustomerOrderLine
from endpoints.customer_order_line.resource import customer_order_line_fields

from endpoints.customer_order.resource import CustomerOrderResource
from endpoints.customer_order.model import CustomerOrder
from endpoints.customer_order.resource import customer_order_fields

from endpoints.weather.resource import WeatherResource
from endpoints.weather.model import Weather
from endpoints.weather.resource import weather_fields

"""
Adding all the resources needed
Actions: POST, GET, PUT, DELETE
"""
api.add_resource(CustomerOrderLineResource, '/customer-order-lines', '/customer-order-line/<int:customer_order_line_id>')
api.add_resource(CustomerOrderResource, '/customer-orders', '/customer-order/<int:customer_order_id>')
api.add_resource(WeatherResource, '/weathers', '/weather/<int:weather_id>')

"""
Non resource endpoints
"""

@app.route('/api/get-customer-order-status/', methods=['GET'])
def customer_order_status():
    priority = {
        'CANCELLED': 1,
        'SHIPPED': 2,
        'PENDING': 3,
    }
    def get_value(dicc):
        return dicc['order_number']
    customer_order_line = CustomerOrderLine.query.all()
    customer_ord_lines = marshal(customer_order_line, customer_order_line_fields)
    customer_ord_lines = groupby(customer_ord_lines, get_value)
    result = {key: max(list(value), key=lambda item: priority[item['status']])['status'] for key, value in customer_ord_lines}
    return jsonify({'customer_ord_status': result})

spring = range(77, 178)
summer = range(178, 265)
fall = range(265, 355)

@app.route('/api/get-seasons/', methods=['GET'])
def seasons():
    def get_season(date):
        day =  date.timetuple().tm_yday

        if day in spring:
            return 'Spring'
        elif day in summer:
            return 'Summer'
        elif day in fall:
            return 'Fall'
        else:
            return 'Winter'
    customer_orders = CustomerOrder.query.all()
    customer_orders = marshal(customer_orders, customer_order_fields)
    result = {item['ord_id'] : get_season(datetime.strptime(item['ord_dt'], '%m/%d/%y')) for item in customer_orders}
    return jsonify({'seasons': result})

@app.route('/api/detect-change/', methods=['GET'])
def detecting_change():
    weather = Weather.query.order_by(Weather.id).all()
    weather = marshal(weather, weather_fields)
    result = []
    prev = False
    for i in weather:
        if prev == False and i['was_rainy']:
            prev = True
            result.append(i)
        prev = i['was_rainy']

    return jsonify({'seasons': result})

if __name__ == '__main__':
    app.run()
