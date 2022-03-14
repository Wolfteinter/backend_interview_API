from flask_restful import Resource, reqparse, request
from flask_restful import fields, marshal_with, marshal
from .model import Weather
from app import db

weather_fields = {
    'id': fields.Integer,
    'date': fields.String,
    'was_rainy': fields.Boolean
    
}

weather_list_fields = {
    'count': fields.Integer,
    'weathers': fields.List(fields.Nested(weather_fields)),
}

weather_post_parser = reqparse.RequestParser()
weather_post_parser.add_argument('date', type=str, required=True, location=['json'],help='name parameter is required')
weather_post_parser.add_argument('was_rainy', type=bool, required=True, location=['json'],help='name parameter is required')


class WeatherResource(Resource):
    def get(self, weather_id=None):
        if weather_id:
            weather = Weather.query.filter_by(id=weather_id).first()
            return marshal(weather, weather_fields)
        else:
            args = request.args.to_dict()
            limit = args.get('limit', 0)
            offset = args.get('offset', 0)

            args.pop('limit', None)
            args.pop('offset', None)

            weather = Weather.query.filter_by(**args).order_by(Weather.id)

            if limit:
                weather = weather.limit(limit)

            if offset:
                weather = weather.offset(offset)

            weather = weather.all()

            return marshal({
                'count': len(weather),
                'weathers': [marshal(u, weather_fields) for u in weather]
            }, weather_list_fields)

    @marshal_with(weather_fields)
    def post(self):
        args = weather_post_parser.parse_args()

        weather = Weather(**args)
        db.session.add(weather)
        db.session.commit()

        return weather

    @marshal_with(weather_fields)
    def put(self, weather_id=None):
        weather = Weather.query.get(weather_id)

        if 'date' in request.json:
            weather.date = request.json['date']

        if 'was_rainy' in request.json:
            weather.was_rainy = request.json['was_rainy']

        db.session.commit()
        return weather

    @marshal_with(weather_fields)
    def delete(self, weather_id=None):
        weather = Weather.query.get(weather_id)

        db.session.delete(weather)
        db.session.commit()

        return weather
