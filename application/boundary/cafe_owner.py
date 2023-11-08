from flask import Blueprint, render_template, redirect, url_for, session, abort, request, flash
from application.control.const import CAFE_OWNER
from application.control.workslots import WorkSlots

owner = Blueprint("owner", __name__, url_prefix="/owner")

wController = WorkSlots()


@owner.before_request
def check_user_validity():
    if 'user_id' not in session:
        return redirect(url_for("boundary.auth.login"))

    if session['user_type'] != CAFE_OWNER:
        return abort(403)


@owner.route("/")
def view_work_slots():

    slots = wController.get_upcoming_workslots()

    return render_template("./cafe_owner/view_work_slots.html"
                           , title="Upcoming Work Slots"
                           , page_for="Upcoming"
                           , slots=slots)


@owner.route("/create-work-slot", methods=['GET', 'POST'])
def create_work_slot():

    work_slots_dates = wController.get_dates_range()
    shifts = wController.get_shifts()

    if request.method == 'POST':
        shift = request.form.get('shift')
        date = request.form.get('date')

        stat = wController.create_work_slot(shift, date)

        flash("Record Added Successfully")
        return redirect(url_for("boundary.owner.create_work_slot"))

    return render_template("./cafe_owner/create_work_slots.html"
                           , work_slots_dates=work_slots_dates
                           , shifts=shifts
                           , title="Create Work Slot")


@owner.route("/view-all-work-slot")
def view_all_work_slot():

    slots = wController.get_all_work_slots()

    return render_template("./cafe_owner/view_work_slots.html"
                           , title="View All Work Slots"
                           , slots=slots)


@owner.route("/update-work-slot/<int:slot_id>", methods=['GET', 'POST'])
def update_work_slot(slot_id):

    if request.method == 'POST':
        shift = request.form.get('shift')
        date = request.form.get('date')

        wController.update_slot(slot_id, shift, date)

        return redirect(url_for("boundary.owner.view_work_slots"))

    work_slots_dates = wController.get_dates_range()
    shifts = wController.get_shifts()

    slot = wController.get_work_slot_by_id(slot_id)


    return render_template("./cafe_owner/create_work_slots.html"
                           , work_slots_dates=work_slots_dates
                           , shifts=shifts
                           , title="Update Work Slot"
                           , slot=slot)


@owner.route("/delete-work-slot/<int:work_slot_id>")
def delete_work_slot(work_slot_id):

    wController.delete_work_slot(work_slot_id)

    flash("Deleted Successfully")
    return redirect(url_for("boundary.owner.view_work_slots"))