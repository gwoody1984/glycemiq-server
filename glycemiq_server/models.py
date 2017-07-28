from glycemiq_server import db


class UserToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(6), nullable=False)
    access_token = db.Column(db.Text, nullable=False)
    refresh_token = db.Column(db.Text, nullable=False)
    expires_at = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return "<UserToken '{}': '{}'>".format(self.id, self.user_id)
