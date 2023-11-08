import datetime
from datetime import date, timedelta
from application.entity.work_slot import WorkSlotsEntity


class WorkSlots:

    _workSlotEntity = WorkSlotsEntity()

    MORNING = {
        "shift": "Morning",
        "time-start": datetime.time(hour=9),
        "time-end": datetime.time(hour=15)
    }

    EVENING = {
        "shift": "Evening",
        "time-start": datetime.time(hour=15),
        "time-end": datetime.time(hour=21)
    }
    SHIFTS = [MORNING, EVENING]

    RECORD_ADDED_SUCCESSFULLY = "RECORD_ADDED_SUCCESSFULLY"

    def get_work_slot_by_id(self, slot_id):
        return self._workSlotEntity.get_work_slot(slot_id=slot_id)

    def get_dates_range(self, start=date.today(), end=date.today() + timedelta(days=6)):
        date_list = []
        curr_date = start
        while curr_date <= end:
            date_list.append(curr_date)
            curr_date += timedelta(days=1)

        return date_list

    def get_shifts(self):
        return self.SHIFTS

    def create_work_slot(self, shift, date):
        date_obj = datetime.datetime.strptime(date, "%d/%b/%y")
        self._workSlotEntity.add_work_slot(date_obj, shift)

        # TODO: CHECK IF WORK SLOT IS ALREADY BEEN CREATED

        return self.RECORD_ADDED_SUCCESSFULLY

    def update_slot(self, id, shift, date):
        date_obj = datetime.datetime.strptime(date, "%d/%b/%y")
        self._workSlotEntity.update_work_slot(id, shift, date_obj)

        return self.RECORD_ADDED_SUCCESSFULLY

    def get_all_work_slots(self):
        return self._workSlotEntity.get_work_slots()

    def get_upcoming_workslots(self):
        date = datetime.date.today()
        return self._workSlotEntity.get_work_slots(date=date)

    def delete_work_slot(self, slot_id):
        self._workSlotEntity.delete_work_slot(slot_id)