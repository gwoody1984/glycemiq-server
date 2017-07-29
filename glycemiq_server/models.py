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
    collection_type = db.Column(db.String(25), nullable=False)
    date = db.Column(db.Date, nullable=False)
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
    resting_heart_rate = db.Column(db.Integer, nullable=False)
    sedentary_minutes = db.Column(db.Integer, nullable=False)
    lightly_active_minutes = db.Column(db.Integer, nullable=False)
    fairly_active_minutes = db.Column(db.Integer, nullable=False)
    very_active_minutes = db.Column(db.Integer, nullable=False)
    calories_out = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Activity '{:%Y-%m-%d}': '{}'>".format(self.date, self.user_id)


class Body(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_date = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.String(6), nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    fat_percent = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<Body '{:%Y-%m-%d}': '{}'>".format(self.date, self.user_id)


class SleepSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_date = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.String(6), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    efficiency = db.Column(db.Integer, nullable=False)
    minutes_asleep = db.Column(db.Integer, nullable=False)
    minutes_awake = db.Column(db.Integer, nullable=False)
    is_main_sleep = db.Column(db.Boolean, nullable=False)
    details = db.relationship('SleepDetail', backref='sleep_summary', lazy='dynamic')

    def __repr__(self):
        return "<SleepSummary '{:%Y-%m-%d}': '{}' '{}'>".format(
            self.date,
            self.user_id,
            "Main Sleep" if self.is_main_sleep else "Not Main Sleep"
        )


class SleepDetail(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sleep_summary_id = db.Column(db.Integer, db.ForeignKey('sleep_summary.id'), nullable=False)
    data_point_time = db.Column(db.DateTime, nullable=False)
    level = db.Column(db.String(10), nullable=False)
    seconds = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<SleepDetail '{:%Y-%m-%d %H:%M:%S}': '{}' '{}s'>".format(
            self.data_point_time,
            self.level,
            self.seconds
        )
