from datetime import datetime
from glycemiq_server import db


class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(6), nullable=False)
    access_token = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<UserToken '{}': '{}'>".format(self.id, self.user_id)


class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_date = db.Column(db.DateTime, default=datetime.utcnow)
    collection_Type = db.Column(db.String(25), nullable=False)
    date =db.Column(db.Date, nullable=False)
    user_id = db.Column(db.String(6), nullable=False)
    owner_type = db.Column(db.String(25), nullable=False)
    subscription_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Notification '{:%Y-%m-%d}' '{}': '{}'>".format(self.date, self.collection_Type, self.user_id)
