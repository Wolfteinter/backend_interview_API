from app import db


class Weather(db.Model):
    __tablename__ = 'weather'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20))
    was_rainy = db.Column(db.Boolean)
    def __repr__(self):
        return 'Id: {}, date: {}'.format(self.id, self.date)