import datetime

from .models import WorkSlot
from application.entity import db


class WorkSlotsEntity:
    def add_work_slot(self, date, shift):
        slot = WorkSlot(date=date, shift_time=shift)
        db.session.add(slot)
        db.session.commit()

    def get_work_slots(self, date=None):
        workSlot = WorkSlot.query
        if not date:
            workSlot = workSlot.order_by(WorkSlot.date.desc())
        else:
            workSlot = workSlot.filter(WorkSlot.date >= datetime.date.today()).all()

        return workSlot

    def get_work_slot(self, slot_id=None):
        return WorkSlot.query.get_or_404(slot_id)

    def update_work_slot(self, id, shift, date):
        slot = WorkSlot.query.get_or_404(id)
        slot.shift_time = shift
        slot.date = date
        db.session.commit()


    def delete_work_slot(self, slot_id):
        slot = WorkSlot.query.get_or_404(slot_id)
        db.session.delete(slot)
        db.session.commit()