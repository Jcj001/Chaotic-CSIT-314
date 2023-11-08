from flask import Blueprint, render_template, request, session, redirect, url_for, abort, flash
from application.control.const import ACCESS_LEVELS, SYSTEM_ADMIN, CAFE_OWNER, CAFE_STAFF, CAFE_MANAGER
from application.control.user import UserController

admin = Blueprint("admin", __name__, url_prefix="/admin")


@admin.before_request
def check_user_validity():
    if 'user_id' not in session:
        return redirect(url_for("boundary.auth.login"))

    if session['user_type'] != SYSTEM_ADMIN:
        return abort(403)


@admin.route("/")
def dashboard():

    userController = UserController()
    login_info = userController.get_user_login_info()

    all_users = userController.get_all_users()
    user_counts = {
        SYSTEM_ADMIN: 0,
        CAFE_STAFF: 0,
        CAFE_MANAGER: 0,
        CAFE_OWNER: 0,
        "TOTAL": 0
    }

    for user in all_users:
        user_counts[user.user_type] = user_counts[user.user_type] + 1
        user_counts['TOTAL'] = user_counts['TOTAL'] + 1

    return render_template("system_admin/dashboard.html"
                           , login_info=login_info
                           , user_counts=user_counts)


@admin.route("/create-user-account", methods=['GET', 'POST'])
def create_user_account():

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        access_level = request.form.get('access_level')

        auth = UserController()
        authStatus = auth.add_user(email, password, access_level)

        if authStatus == auth.RECORD_ADDED_SUCCESSFULLY:
            flash("User Added Successfully")
        else:
            flash("Something went wrong!")

        return redirect(url_for("boundary.admin.create_user_account"))

    return render_template("system_admin/create_user_account.html"
                           , ACCESS_LEVELS=ACCESS_LEVELS
                           , title="Create User Account")


@admin.route("/create-user-profile", methods=['GET', 'POST'])
def create_user_profile():


    userController = UserController()

    all_accounts = userController.get_all_new_users()

    if request.method == 'POST':
        account = request.form.get('account')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        designation = request.form.get('designation')
        salary = request.form.get('salary')

        status = userController.add_user_profile(account, first_name, last_name, phone_number, designation, salary)
        if status == userController.RECORD_ADDED_SUCCESSFULLY:
            flash("Profile Added Successfully")
        else:
            flash("Something went wrong!")
        return redirect(url_for('boundary.admin.create_user_profile'))

    return render_template("system_admin/create_user_profile.html"
                           , all_accounts=all_accounts
                           , title="Create User Profile")


@admin.route("/view-user-accounts")
def view_user_accounts():

    email = request.args.get("q", None, type=str)

    usersController = UserController()

    if email:
        users = usersController.get_user(email=email)
        users = [users]
    else:
        users = usersController.get_all_users()

    return render_template("system_admin/view-user-accounts.html"
                           , users=users
                           , title="View User Accounts")


@admin.route("/view-suspended-user-accounts")
def view_suspended_user_accounts():

    usersController = UserController()
    users = usersController.get_suspended_accounts()

    return render_template("system_admin/view-user-accounts.html"
                           , users=users
                           , title="View Suspended User Accounts")


@admin.route("/view-user-profiles")
def view_user_profiles():

    name = request.args.get("q", None, type=str)

    usersController = UserController()
    if name:
        users = usersController.search_user(name)
    else:
        users = usersController.get_all_users(complete_profile=True)

    return render_template("system_admin/view-user-profiles.html"
                           , users=users)


@admin.route("/delete-user-account/<int:account_id>")
def delete_user_account(account_id):
    userController = UserController()
    status = userController.delete_user_account(account_id)

    if status == userController.USER_NOT_FOUND:
        flash("Account Not Found")
    else:
        flash("Deleted Successfully")
    return redirect(url_for("boundary.admin.view_user_accounts"))


@admin.route("/suspend-user-account/<int:account_id>")
def suspend_user_account(account_id):
    userController = UserController()
    status = userController.suspend_user_account(account_id)

    if status == userController.USER_NOT_FOUND:
        flash("Account Not Found")
    else:
        flash("Suspended Successfully")
    return redirect(url_for("boundary.admin.view_user_accounts"))


@admin.route("/unsuspend-user-account/<int:account_id>")
def unsuspend_user_account(account_id):
    userController = UserController()
    status = userController.unsuspend_user_account(account_id)

    if status == userController.USER_NOT_FOUND:
        flash("Account Not Found")
    else:
        flash("Suspended Successfully")
    return redirect(url_for("boundary.admin.view_user_accounts"))


@admin.route("/update-user-account/<int:account_id>", methods=['GET', 'POST'])
def update_user_account(account_id):
    userController = UserController()
    user = userController.get_user(account_id=account_id)

    if request.method == "POST":
        email = request.form.get('email')
        password = request.form.get('password')
        access_level = request.form.get('access_level')

        userController.update_user_account(account_id, email, password, access_level)

        return redirect(url_for("boundary.admin.view_user_accounts"))

    return render_template("system_admin/create_user_account.html"
                           , user=user
                           , title="Update User Account"
                           , ACCESS_LEVELS=ACCESS_LEVELS)


@admin.route("/update-user-profile/<int:account_id>", methods=['GET', 'POST'])
def update_user_profile(account_id):
    userController = UserController()
    user = userController.get_user(account_id=account_id)

    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        phone_number = request.form.get('phone_number')
        designation = request.form.get('designation')
        salary = request.form.get('salary')

        status = userController.add_user_profile(account_id, first_name, last_name, phone_number, designation, salary)
        if status == userController.RECORD_ADDED_SUCCESSFULLY:
            flash("Profile Added Successfully")
        else:
            flash("Something went wrong!")
        return redirect(url_for('boundary.admin.view_user_profiles'))

    return render_template("system_admin/create_user_profile.html"
                           , user=user
                           , title="Update User Profile"
                           , ACCESS_LEVELS=ACCESS_LEVELS)