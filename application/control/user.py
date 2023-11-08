import datetime

from flask import session
from application.entity.user import UserEntity
from .const import ACCESS_LEVELS

logged_in_users = dict()

class UserController:
    _userEntity = UserEntity()

    USER_NOT_FOUND = "USER_NOT_FOUND"
    INVALID_PASSWORD = "INVALID_PASSWORD"
    USER_NOT_LOGGED_IN = "USER_NOT_LOGGED_IN"
    INVALID_ACCESS_LEVEL = "INVALID_ACCESS_LEVEL"
    RECORD_ADDED_SUCCESSFULLY = "RECORD_ADDED_SUCCESSFULLY"
    CANNOT_REMOVE_SELF = "CANNOT_REMOVE_SELF"
    SUSPENDED_ACCOUNT = "SUSPENDED_ACCOUNT"

    def authenticate(self, email: str, password: str):
        user = self._userEntity.get_user_by_email(email=email)
        if not user:
            return self.USER_NOT_FOUND

        if user.password != password:
            return self.INVALID_PASSWORD

        if user.account_status == "SUSPENDED":
            return self.SUSPENDED_ACCOUNT

        return user

    def get_user(self, account_id=None, email=None):
        if account_id:
            user = self._userEntity.get_user_by_id(account_id)
            return user
        elif email:
            user = self._userEntity.get_user_by_email(email)
            return user

    def login_user(self, user_id: int, user_type: str):
        session['user_id'] = user_id
        session['user_type'] = user_type

        user = self.get_user(account_id=user_id)

        email = user.email
        full_name = user.first_name + f" {user.last_name}" if user.last_name else ""

        logged_in_users[user_id] = {
            "user_id": user_id,
            "full_name": full_name,
            "email": email,
            "last_login": "Active",
            "user_type": user_type
        }

    def logout_user(self):
        if 'user_id' in session:

            user = logged_in_users.get(session['user_id'])
            if user:
                user['last_login'] = datetime.datetime.now().strftime("%d/%b - %H:%M")

            session.pop('user_id')
            session.pop('user_type')

    def get_user_login_info(self):
        return logged_in_users

    def get_user_type(self):
        if 'user_id' in session:
            return session['user_type']
        
        return self.USER_NOT_LOGGED_IN

    def add_user(self, email: str, password: str, user_type: str):
        if user_type not in ACCESS_LEVELS:
            return self.INVALID_ACCESS_LEVEL

        self._userEntity.add_user_account(email, password, user_type)
        return self.RECORD_ADDED_SUCCESSFULLY

    def add_user_profile(self, account_id, first_name, last_name, phone_number, designation, salary):
        self._userEntity.update_user_profile(account_id, first_name, last_name, phone_number, designation, salary)
        return self.RECORD_ADDED_SUCCESSFULLY

    def get_all_users(self, complete_profile=False):
        if complete_profile:
            return self._userEntity.get_all_complete_profile_user()
        return self._userEntity.get_all_users()

    def get_all_new_users(self):
        return self._userEntity.get_all_new_user()

    def delete_user_account(self, account_id):

        if session['user_id'] == account_id:
            return

        status = self._userEntity.delete_user_account_by_id(account_id)
        if status == self._userEntity.USER_NOT_FOUND:
            return self.USER_NOT_FOUND
        return self.RECORD_ADDED_SUCCESSFULLY

    def suspend_user_account(self, account_id):
        if session['user_id'] == account_id:
            return self.CANNOT_REMOVE_SELF

        SUSPENDED = "SUSPENDED"

        status = self._userEntity.set_account_status(account_id, SUSPENDED)
        if status == self._userEntity.USER_NOT_FOUND:
            return self.USER_NOT_FOUND

        return self.RECORD_ADDED_SUCCESSFULLY

    def unsuspend_user_account(self, account_id):
        if session['user_id'] == account_id:
            return self.CANNOT_REMOVE_SELF

        UNSUSPENDED = ""

        status = self._userEntity.set_account_status(account_id, UNSUSPENDED)
        if status == self._userEntity.USER_NOT_FOUND:
            return self.USER_NOT_FOUND

        return self.RECORD_ADDED_SUCCESSFULLY

    def get_suspended_accounts(self):
        return self._userEntity.get_user_by_account_status("SUSPENDED")

    def update_user_account(self, account_id, email, password, access_level):
        status = self._userEntity.update_user_account(account_id, email, password, access_level)

        if status == self._userEntity.USER_NOT_FOUND:
            return self.USER_NOT_FOUND

        return self.RECORD_ADDED_SUCCESSFULLY

    def search_user(self, name=None):
        if name:
            return self._userEntity.search_user_by_name(name)