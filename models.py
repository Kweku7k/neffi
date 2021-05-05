from app import db

class User(db.Model):
    tablename = ['User']
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(200), nullable=False)
    lastname = db.Column(db.String(), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f"User('{self.lastname}', '{self.email}', '{self.phone}')"


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String())
    skillGroup = db.Column(db.String())
    q_number = db.Column(db.String())