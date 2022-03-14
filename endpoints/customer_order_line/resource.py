from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import CustomerOrderLine
from app import db

customer_order_line_fields = {
    'id': fields.Integer,
    'order_number': fields.String,
    'item_name': fields.String,
    'status': fields.String
    
}

customer_order_line_list_fields = {
    'count': fields.Integer,
    'customer_order_line': fields.List(fields.Nested(customer_order_line_fields)),
}

customer_order_line_post_parser = reqparse.RequestParser()
customer_order_line_post_parser.add_argument('order_number', type=str, required=True, location=['json'],help='name parameter is required')
customer_order_line_post_parser.add_argument('item_name', type=str, required=True, location=['json'],help='name parameter is required')
customer_order_line_post_parser.add_argument('status', type=str, required=True, location=['json'],help='name parameter is required')


class CustomerOrderLineResource(Resource):
    def get(self, customer_order_line_id=None):
        if customer_order_line_id:
            customer_order_line = CustomerOrderLine.query.filter_by(id=customer_order_line_id).first()
            return marshal(customer_order_line, customer_order_line_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            customer_order_line = CustomerOrderLine.query.filter_by(**args).order_by(CustomerOrderLine.id)

            if limit:
                customer_order_line = customer_order_line.limit(limit)

            if offset:
                customer_order_line = customer_order_line.offset(offset)

            customer_order_line = customer_order_line.all()

            return marshal({
                'count': len(customer_order_line),
                'customer_order_line': [marshal(u, customer_order_line_fields) for u in customer_order_line]
            }, customer_order_line_list_fields)

    @marshal_with(customer_order_line_fields)
    def post(self):
        args = customer_order_line_post_parser.parse_args()

        customer_order_line = CustomerOrderLine(**args)
        db.session.add(customer_order_line)
        db.session.commit()

        return customer_order_line

    @marshal_with(customer_order_line_fields)
    def put(self, customer_order_line_id=None):
        customer_order_line = CustomerOrderLine.query.get(customer_order_line_id)

        if 'order_number' in request.json:
            customer_order_line.order_number = request.json['order_number']

        if 'item_name' in request.json:
            customer_order_line.item_name = request.json['item_name']

        if 'status' in request.json:
            customer_order_line.status = request.json['status']

        db.session.commit()
        return customer_order_line

    @marshal_with(customer_order_line_fields)
    def delete(self, customer_order_line_id=None):
        customer_order_line = CustomerOrderLine.query.get(customer_order_line_id)

        db.session.delete(customer_order_line)
        db.session.commit()

        return customer_order_line
