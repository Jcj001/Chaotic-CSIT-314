from flask import Blueprint, render_template, request, flash, redirect, url_for
from application.control.user import UserController
from application.control.const import SYSTEM_ADMIN, CAFE_OWNER

authentication = Blueprint("auth", __name__)


@authentication.route("/", methods=['GET', 'POST'])
@authentication.route("/login", methods=['GET', 'POST'])
def login():


    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        auth = UserController()
        authStatus = auth.authenticate(email, password)

        if authStatus == auth.USER_NOT_FOUND:
            flash("User doesn't exist")
            return redirect(url_for("boundary.auth.login"))
        elif authStatus == auth.INVALID_PASSWORD:
            flash("Invalid Password")
            return redirect(url_for("boundary.auth.login"))
        elif authStatus == auth.SUSPENDED_ACCOUNT:
            flash("Your Account is Suspended")
            return redirect(url_for("boundary.auth.login"))

        auth.login_user(authStatus.id, authStatus.user_type)
        
        if authStatus.user_type == SYSTEM_ADMIN:
            return redirect(url_for('boundary.admin.dashboard'))
        elif authStatus.user_type == CAFE_OWNER:
            return redirect(url_for('boundary.owner.view_work_slots'))

    return render_template("login.html")


@authentication.route("/logout")
def logout():
    userController = UserController()
    userController.logout_user()

    return redirect(url_for("boundary.auth.login"))