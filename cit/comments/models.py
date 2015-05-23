from ..db import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    issue_id = db.Column(db.Integer, db.ForeignKey("issue.id"))
    message = db.Column(db.String(400))

    author = db.relationship("User")
    issue = db.relationship("Issue")

    def __init__(self, author="", issue="", message=""):
        self.author = author
        self.issue = issue
        self.message = message

    def __repr__(self):
        return '<message %r>' % self.message