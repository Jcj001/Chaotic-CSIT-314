from sqlalchemy import or_

from .models import User
from application.entity import db


class UserEntity:

    USER_NOT_FOUND = "USER_NOT_FOUND"

    def get_user_by_email(self, email: str):
        user = User.query.filter(User.email==email).first()
        return user

    def get_user_by_id(self, id):
        user = User.query.get(id)
        return user

    def get_all_users(self):
        return User.query.all()

    def get_all_complete_profile_user(self):
        return User.query.filter(User.first_name != None).all()

    def get_all_new_user(self):
        return User.query.filter(User.first_name==None).all()

    def add_user_account(self, email: str, password: str, user_type: str):
        user = User(email=email, password=password, user_type=user_type)
        db.session.add(user)
        db.session.commit()

    def update_user_profile(self, account_id, first_name, last_name, phone_number, designation, salary):
        user = User.query.get(account_id)
        if not user:
            return False

        user.first_name = first_name
        user.last_name = last_name
        user.phone_number = phone_number
        user.designation = designation
        user.salary = salary

        db.session.commit()

        return True

    def delete_user_account_by_id(self, account_id):
        try:
            user = User.query.get_or_404(account_id)
        except:
            return self.USER_NOT_FOUND

        print("Deleting")
        db.session.delete(user)
        db.session.commit()

        return True

    def set_account_status(self, account_id, status):
        try:
            user = User.query.get_or_404(account_id)
        except:
            return self.USER_NOT_FOUND

        user.account_status = status
        db.session.commit()
        return True

    def get_user_by_account_status(self, status):
        return User.query.filter(User.account_status == status).all()

    def update_user_account(self, account_id, email, password, access_level):
        try:
            user = User.query.get_or_404(account_id)
        except:
           return self.USER_NOT_FOUND

        user.email = email
        user.password = password
        user.user_type = access_level

        db.session.commit()

        return True

    def search_user_by_name(self, name):
        return User.query.filter(or_(User.first_name.like(f"%{name}%")
                                     , User.last_name.like(f"%{name}%") )).all()
