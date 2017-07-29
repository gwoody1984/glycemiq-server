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
    subscription_id = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return "<Notification '{:%Y-%m-%d}' '{}': '{}'>".format(self.date, self.collection_Type, self.user_id)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_date = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.String(6), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    restingHeartRate = db.Column(db.Integer, nullable=False)
    sedentaryMinutes = db.Column(db.Integer, nullable=False)
    lightlyActiveMinutes = db.Column(db.Integer, nullable=False)
    fairlyActiveMinutes = db.Column(db.Integer, nullable=False)
    veryActiveMinutes = db.Column(db.Integer, nullable=False)
    caloriesOut = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Activity '{:%Y-%m-%d}': '{}'>".format(self.date, self.user_id)
