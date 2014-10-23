from app import db

class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    to_number = db.Column(db.String(30))
    from_number = db.Column(db.String(30))
    text = db.Column(db.String())
    time_sent = db.Column(db.DateTime, default=db.func.now())

    def __repr__(self):
        return '<Message %r>' % (self.text)
