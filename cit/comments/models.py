from ..db import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    message = db.Column(db.String(400))

    def __init__(self, message=""):
        self.message = message

    def __repr__(self):
        return '<message %r>' % self.message