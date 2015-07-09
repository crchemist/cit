from ..db import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    message = db.Column(db.String(400))

    author = db.relationship('User')
    issue = db.relationship('Issue')

    def __init__(self, author_id=None, issue_id=None, message=''):
        self.author_id = author_id
        self.issue_id = issue_id
        self.message = message

    def __repr__(self):
        return '%r' % self.message
