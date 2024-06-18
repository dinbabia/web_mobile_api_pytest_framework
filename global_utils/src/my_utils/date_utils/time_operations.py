from datetime import datetime, timedelta, time
from typing import List

from my_utils.date_utils.datetime_formatter import DateTimeFormatters


class TimeFacade:

    def __init__(self) -> None:
        """
        When instantiated, start and end time will have current year, month, and day with:
        start_time - 08:00 | 24 hour format.
        end_time   - 20:00 | 24 hour format.
        """
        self._time_operations = TimeOperations
        self._time_filters = TimeFilters

        self.start_time = self._time_operations.create_time_object(hour=8, minute=0)
        self.end_time = self._time_operations.create_time_object(hour=20, minute=0)

        self._total_time_slots = self._time_operations.get_all_time_within_a_span(self.start_time, self.end_time)
        self._current_available_time_slots = self._total_time_slots

    def _set_time_using_string_process(self, time_string: str) -> datetime:
        dt_obj = DateTimeFormatters.convert_time_string_to_datetime([time_string])
        return dt_obj[0]

    def set_start_time_using_integers(self, hour: int, minute: int) -> datetime:
        self.start_time = self._time_operations.create_time_object(hour, minute)

    def set_end_time_using_integers(self, hour: int, minute: int) -> datetime:
        self.end_time = self._time_operations.create_time_object(hour, minute)

    def set_start_time_using_strings(self, start_time: str) -> None:
        self.start_time = self._set_time_using_string_process(start_time)

    def set_end_time_using_strings(self, end_time: str) -> None:
        self.end_time = self._set_time_using_string_process(end_time)

    def create_time_object_with_integers(self, hour: int, minute: int) -> datetime:
        return self._time_operations.create_time_object(hour=hour, minute=minute)

    def get_all_time_from_start_to_end_range(self) -> List[datetime]:
        self._current_available_time_slots = self._time_operations.get_all_time_within_a_span(self.start_time, self.end_time)
        return self._current_available_time_slots

    def get_all_time_from_start_to_end_with_existing_time_filters(self, existing_time_slots: dict) -> List[datetime]:
        self._current_available_time_slots = self._time_filters.filter_time_slots_with_existing_time_slots(self._current_available_time_slots, existing_time_slots)
        return self._current_available_time_slots

    def get_all_time_from_start_to_end_with_service_filters(self, service_duration: int) -> List[datetime]:
        self._current_available_time_slots = self._time_filters.filter_time_slots_with_a_service_duration(self._current_available_time_slots, service_duration)
        return self._current_available_time_slots

    def get_all_time_from_start_to_end_with_optimized_filters(self, optimised_time: int) -> List[datetime]:
        self._current_available_time_slots = self._time_filters.filter_time_slots_with_optimized_booking(self._current_available_time_slots, optimised_time)
        return self._current_available_time_slots


class TimeOperations:

    @staticmethod
    def create_time_object(hour: int = 0, minute: int = 0) -> datetime:
        current_date = datetime.now()
        dt = datetime(year=current_date.year, month=current_date.month, day=current_date.day, hour=hour, minute=minute)
        return dt

    @staticmethod
    def get_all_time_within_a_span(start_time: datetime, end_time: datetime) -> List[datetime]:
        time_list = []
        while start_time <= end_time:

            time_slot = start_time + timedelta(minutes=15)
            if time_slot <= end_time:
                time_list.append(start_time)
                start_time += timedelta(minutes=15)
            else:
                break
        return time_list

    @staticmethod
    def get_end_time_using_integer_duration(start_datetime: datetime, duration: int) -> datetime:
        return start_datetime + timedelta(minutes=duration)


class TimeFilters:

    @staticmethod
    def filter_time_slots_with_existing_time_slots(available_time_slots: List[datetime], existing_time_slots: List[dict]) -> List[datetime]:
        for time_slot in existing_time_slots:
            if time_slot['has_processing_time']:
                available_time_slots = TimeFilters._filter_with_processing_time(time_slot, available_time_slots)
            else:
                available_time_slots = TimeFilters._filter_with_no_processing_time(time_slot, available_time_slots)
        return available_time_slots

    @staticmethod
    def _filter_with_processing_time(time_slot: dict, available_time_slots: List[datetime]):
        processing_start_time = time_slot['start_time'] + timedelta(minutes=time_slot['application_time'])
        processing_end_time = processing_start_time + timedelta(minutes=time_slot['processing_time'])
        finishing_end_time = processing_end_time + timedelta(minutes=time_slot['finishing_time'])
        # Remove all timeslots within range of | start_time -> end of application time
        # Remove all timeslots within range of | processing end time -> finishing end time
        return [available_time for available_time in available_time_slots
                if not (
                    TimeFilters._is_time_in_range(time_slot['start_time'], processing_start_time, available_time) or
                    TimeFilters._is_time_in_range(processing_end_time, finishing_end_time, available_time))]

    @staticmethod
    def _filter_with_no_processing_time(time_slot: dict, available_time_slots: List[datetime]):
        end_datetime = time_slot['start_time'] + timedelta(minutes=time_slot['duration'])
        # Remove all timeslots within the start and end time range
        return [avaialable_time for avaialable_time in available_time_slots if not (time_slot['start_time'] <= avaialable_time < end_datetime)]

    @staticmethod
    def _is_time_in_range(start: time, end: time, check: time) -> bool:
        return start <= check < end

    @staticmethod
    def filter_time_slots_with_a_service_duration(available_slots: List[datetime], service_duration: int) -> List[datetime]:
        # Rules and Logic:
        # 1. We need to know the whole service time range by adding the 'time_slot' and 'duration' to
        # check whether it can accomodate the whole service duration.
        # 2. This can be done by checking if all the time slots with 15mins increment
        # within the whole duration are in the available slots (meaning it can accomodate the whole service duration)
        def is_valid_time_slot(time_slot: datetime) -> bool:
            end_time = time_slot + timedelta(minutes=service_duration)
            current_time = time_slot

            # check if time_slot is valid (by adding 15 mins per iteration) until ...
            # the whole service duration is exhausted (end_time)
            while current_time < end_time:
                if current_time not in available_slots:
                    # if not exhausted (a time slot is not in the available time slots),
                    # then do not append on the available slots
                    return False
                current_time += timedelta(minutes=15)
            # if exhausted (all time slots are in the available time slots),
            # then it is valid (it can allocate the whole time duration)
            return True
        return [time_slot for time_slot in available_slots if is_valid_time_slot(time_slot)]

    @staticmethod
    def filter_time_slots_with_optimized_booking(available_slots: List[datetime], optimised_time: int) -> List[datetime]:
        # Step 1 - Group time slots by 15 minutes difference
        # So that we can implement optimised time/booking easily

        # Example:
        # FROM: ['7:15', '7:45', '8:00', '8:30', '8:45', '9:00', '9:30', '9:45', '10:00', '10:15']
        # TO: [ ['7:15'],
        #       ['7:45', '8:00'],
        #       ['8:30', '8:45', '9:00']
        #       ['9:30', '9:45', '10:00', '10:15']]
        grouped_slots = []
        current_group = []

        for i, current_time in enumerate(available_slots):
            current_group.append(current_time)

            # Check if next slot is 15 minutes apart
            if i + 1 < len(available_slots):
                next_time = available_slots[i + 1]
                if next_time - current_time != timedelta(minutes=15):
                    # If next slot is not 15 minutes apart, start a new group
                    grouped_slots.append(current_group)
                    current_group = []
            else:
                # For the last slot, just add the current group
                grouped_slots.append(current_group)
        # Step 2 - Filter out using the optimised booking/time logic
        optimised_slots = []
        time_interval = 15  # Duration of each slot in minutes
        step_counting = int(optimised_time / time_interval)  # Step count when iterating a group

        # Example [
        #   ['7:15'],
        #   ['7:45', '8:00'],
        #   ['8:30', '8:45', '9:00']
        #   ['9:30', '9:45', '10:00', '10:15']]
        # If optimised_time=30, step_counting will be 2 ( from int(optimised_time / time_interval) )
        # NOTE: INDEX 0 WILL ALWAYS BE ADDED, so '7:15', '7:45', '8:30', and '9:30' are added.
        # Since step_counting=2, add all indexes 0, 2, 4, 6 from each group.
        # '9:00' AND '10:00' WILL BE ADDED.
        # '8:00', '8:45', and '9:45' are index 1 so it will NOT BE ADDED.
        # Also '10:15' is index 3 so it will NOT BE ADDED.
        for group in grouped_slots:
            for i in range(0, len(group), step_counting):
                optimised_slots.append(group[i])

        return optimised_slots
