from app import db


class CustomerOrderLine(db.Model):
    __tablename__ = 'customer_order_line'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20))
    item_name = db.Column(db.String(20))
    status = db.Column(db.String(20))
    def __repr__(self):
        return 'Id: {}, order_number: {}'.format(self.id, self.order_number)