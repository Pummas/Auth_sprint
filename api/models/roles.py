from core.config import db


class Role(db.Model):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role %r>' % self.name
