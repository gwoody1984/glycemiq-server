from datetime import datetime
from glycemiq_server import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.Text, nullable=False)
    fitbit_token = db.relationship('FitbitToken', backref='user', lazy='dynamic')
    activities = db.relationship('Activity', backref='user', lazy='dynamic')
    body = db.relationship('Body', backref='user', lazy='dynamic')
    sleep = db.relationship('SleepSummary', backref='user', lazy='dynamic')
    food = db.relationship('Food', backref='user', lazy='dynamic')
    insulin_doses = db.relationship('InsulinDose', backref='user', lazy='dynamic')
    bg_readings = db.relationship('BgReading', backref='user', lazy='dynamic')

    def __repr__(self):
        return "<User '{}': '{}'".format(self.id, self.email)


class FitbitToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    fitbit_user_id = db.Column(db.String(6), nullable=False)
    access_token = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<FitbitToken '{}': '{}'>".format(self.id, self.fitbit_user_id)


class FitbitNotification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    receive_date = db.Column(db.DateTime, default=datetime.utcnow)
    collection_type = db.Column(db.String(25), nullable=False)
    date = db.Column(db.Date, nullable=False)
    fitbit_user_id = db.Column(db.String(6), nullable=False)
    owner_type = db.Column(db.String(25), nullable=False)
    subscription_id = db.Column(db.String(25), nullable=False)

    def __repr__(self):
        return "<Notification '{:%Y-%m-%d}' '{}': '{}'>".format(self.date, self.collection_Type, self.fitbit_user_id)


class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receive_date = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, nullable=False)
    fitbit_user_id = db.Column(db.String(6), nullable=False)
    steps = db.Column(db.Integer, nullable=False)
    resting_heart_rate = db.Column(db.Integer, nullable=False)
    sedentary_minutes = db.Column(db.Integer, nullable=False)
    lightly_active_minutes = db.Column(db.Integer, nullable=False)
    fairly_active_minutes = db.Column(db.Integer, nullable=False)
    very_active_minutes = db.Column(db.Integer, nullable=False)
    calories_out = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<Activity '{:%Y-%m-%d}': '{}'>".format(self.date, self.fitbit_user_id)


class Body(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receive_date = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, nullable=False)
    fitbit_user_id = db.Column(db.String(6), nullable=False)
    bmi = db.Column(db.Float, nullable=False)
    fat_percent = db.Column(db.Float, nullable=False)
    weight = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<Body '{:%Y-%m-%d}': '{}'>".format(self.date, self.fitbit_user_id)


class SleepSummary(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receive_date = db.Column(db.DateTime, default=datetime.utcnow)
    date = db.Column(db.Date, nullable=False)
    fitbit_user_id = db.Column(db.String(6), nullable=False)
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
            self.fitbit_user_id,
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


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receive_date = db.Column(db.DateTime, nullable=False)
    calcium = db.Column(db.Float, nullable=True)
    calcium_unit = db.Column(db.String(5), nullable=True)
    calories = db.Column(db.Float, nullable=True)
    carbs = db.Column(db.Float, nullable=True)
    carbs_unit = db.Column(db.String(5), nullable=True)
    description = db.Column(db.String(5), nullable=True)
    fiber = db.Column(db.Float, nullable=True)
    fiber_unit = db.Column(db.String(5), nullable=True)
    folate = db.Column(db.Float, nullable=True)
    folate_unit = db.Column(db.String(5), nullable=True)
    glycemic_index = db.Column(db.Float, nullable=True)
    iron = db.Column(db.Float, nullable=True)
    iron_unit = db.Column(db.String(5), nullable=True)
    magnesium = db.Column(db.Float, nullable=True)
    magnesium_unit = db.Column(db.String(5), nullable=True)
    measurement = db.Column(db.String(5), nullable=True)
    monounsaturated_fat = db.Column(db.Float, nullable=True)
    monounsaturated_fat_unit = db.Column(db.String(5), nullable=True)
    name = db.Column(db.String(5), nullable=True)
    niacin = db.Column(db.Float, nullable=True)
    niacin_unit = db.Column(db.String(5), nullable=True)
    phosphorus = db.Column(db.Float, nullable=True)
    phosphorus_unit = db.Column(db.String(5), nullable=True)
    polyunsaturated_fat = db.Column(db.Float, nullable=True)
    polyunsaturated_fat_unit = db.Column(db.String(5), nullable=True)
    potassium = db.Column(db.Float, nullable=True)
    potassium_unit = db.Column(db.String(5), nullable=True)
    protein = db.Column(db.Float, nullable=True)
    protein_unit = db.Column(db.String(5), nullable=True)
    quantity = db.Column(db.Float, nullable=True)
    riboflavin = db.Column(db.Float, nullable=True)
    riboflavin_unit = db.Column(db.String(5), nullable=True)
    saturated_fat = db.Column(db.Float, nullable=True)
    saturated_fat_unit = db.Column(db.String(5), nullable=True)
    sodium = db.Column(db.Float, nullable=True)
    sodium_unit = db.Column(db.String(5), nullable=True)
    sugar = db.Column(db.Float, nullable=True)
    sugar_unit = db.Column(db.String(5), nullable=True)
    thiamin = db.Column(db.Float, nullable=True)
    thiamin_unit = db.Column(db.String(5), nullable=True)
    total_fat = db.Column(db.Float, nullable=True)
    total_fat_unit = db.Column(db.String(5), nullable=True)
    vitamin_a = db.Column(db.Float, nullable=True)
    vitamin_a_unit = db.Column(db.String(5), nullable=True)
    vitamin_b6 = db.Column(db.Float, nullable=True)
    vitamin_b6_unit = db.Column(db.String(5), nullable=True)
    vitamin_c = db.Column(db.Float, nullable=True)
    vitamin_c_unit = db.Column(db.String(5), nullable=True)
    vitamin_e = db.Column(db.Float, nullable=True)
    vitamin_e_unit = db.Column(db.String(5), nullable=True)
    vitamin_k = db.Column(db.Float, nullable=True)
    vitamin_k_unit = db.Column(db.String(5), nullable=True)
    zinc = db.Column(db.Float, nullable=True)
    zinc_unit = db.Column(db.String(5), nullable=True)


class InsulinDose(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receive_date = db.Column(db.DateTime, nullable=False)
    insulin_type = db.Column(db.String(5), nullable=False)
    unit_type = db.Column(db.String(5), nullable=False)
    units = db.Column(db.Float, nullable=False)


class BgReading(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    value = db.Column(db.Float, nullable=False)
    receive_date = db.Column(db.DateTime, nullable=False)