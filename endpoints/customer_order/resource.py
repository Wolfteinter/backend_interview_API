from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import CustomerOrder
from app import db
"""
Define serializers
"""
customer_order_fields = {
    'id': fields.Integer,
    'ord_id': fields.String,
    'ord_dt': fields.String,
    'qt_ordd': fields.Integer
}

customer_order_list_fields = {
    'count': fields.Integer,
    'customer_orders': fields.List(fields.Nested(customer_order_fields)),
}
"""
Define the request parser for the post method.
"""
customer_order_post_parser = reqparse.RequestParser()
customer_order_post_parser.add_argument('ord_id', type=str, required=True, location=[
                                        'json'], help='ord_id parameter is required')
customer_order_post_parser.add_argument('ord_dt', type=str, required=True, location=[
                                        'json'], help='ord_dt parameter is required')
customer_order_post_parser.add_argument('qt_ordd', type=str, required=True, location=[
                                        'json'], help='qt_ordd parameter is required')

"""
Define the resource and the methods that will be available
"""


class CustomerOrderResource(Resource):
    """
    Define the GET method
    """

    def get(self, customer_order_id=None):
        if customer_order_id:
            customer_order = CustomerOrder.query.filter_by(
                id=customer_order_id).first()
            return marshal(customer_order, customer_order_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            customer_order = CustomerOrder.query.filter_by(
                **args).order_by(CustomerOrder.id)

            if limit:
                customer_order = customer_order.limit(limit)

            if offset:
                customer_order = customer_order.offset(offset)

            customer_order = customer_order.all()

            return marshal({
                'count': len(customer_order),
                'customer_orders': [marshal(u, customer_order_fields) for u in customer_order]
            }, customer_order_list_fields)
    """
    Define the POST method
    """
    @marshal_with(customer_order_fields)
    def post(self):
        args = customer_order_post_parser.parse_args()

        customer_order = CustomerOrder(**args)
        db.session.add(customer_order)
        db.session.commit()

        return customer_order
    """
    Define the PUT method
    """
    @marshal_with(customer_order_fields)
    def put(self, customer_order_id=None):
        customer_order = CustomerOrder.query.get(customer_order_id)

        if 'ord_id' in request.json:
            customer_order.ord_id = request.json['ord_id']

        if 'ord_dt' in request.json:
            customer_order.ord_dt = request.json['ord_dt']

        if 'qt_ordd' in request.json:
            customer_order.qt_ordd = request.json['qt_ordd']

        db.session.commit()
        return customer_order
    """
    Define the DELETE method
    """
    @marshal_with(customer_order_fields)
    def delete(self, customer_order_id=None):
        customer_order = CustomerOrder.query.get(customer_order_id)

        db.session.delete(customer_order)
        db.session.commit()

        return customer_order
