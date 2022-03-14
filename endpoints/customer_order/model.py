from app import db


class CustomerOrder(db.Model):
    __tablename__ = 'customer_order'

    id = db.Column(db.Integer, primary_key=True)
    ord_id = db.Column(db.String(20))
    ord_dt = db.Column(db.String(20))
    qt_ordd = db.Column(db.String(20))
    def __repr__(self):
        return 'Id: {}, ord_id: {}'.format(self.id, self.order_number)