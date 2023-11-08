from application.entity import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30))
    last_name = db.Column(db.String(30))
    phone_number = db.Column(db.String(20))
    designation = db.Column(db.String(20))
    salary = db.Column(db.Integer)
    email = db.Column(db.String(30), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    user_type = db.Column(db.String(10), nullable=False)
    account_status = db.Column(db.String(10))

    def __repr__(self):
        return f"<User>: {self.email} - {self.user_type}"


class WorkSlot(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    shift_time = db.Column(db.String(10))

    def __repr__(self):
        return f"<WORK SLOT>: {self.date}"