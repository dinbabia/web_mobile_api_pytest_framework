import unittest
from my_utils.date_utils.datetime_formatter import DateTimeFormatters
from my_utils.date_utils.date_operations import DateFacade
from my_utils.date_utils.time_operations import TimeFacade


class TestDateTimeOperations(unittest.TestCase):
    """NOTE:PLEASE ADD ASSERTIONS"""

    datetime_facade = DateFacade()
    time_facade = TimeFacade()

    def test_get_all_days_for_this_month(self):
        # Current Month
        response = self.datetime_facade.get_all_days_for_this_month()
        print(f"Current Month: {response}\n")
        response_2 = self.datetime_facade.get_all_days_with_weekday_filters_for_this_month(weekdays=[0, 1])
        print(f"Filtered Current Month: {response_2}\n")

        # Next Month
        self.datetime_facade.set_datetime_using_integers(year=self.datetime_facade.year, month=self.datetime_facade.month+1)
        response = self.datetime_facade.get_all_days_for_this_month()
        print(f"Next Month: {response}\n")
        response_2 = self.datetime_facade.get_all_days_with_weekday_filters_for_this_month(weekdays=[0, 1])
        print(f"Filtered Next Month: {response_2}\n")

        # November 2024
        self.datetime_facade.set_datetime_using_integers(year=2024, month=11)
        response = self.datetime_facade.get_all_days_for_this_month()
        print(f"November 2024: {response}\n")
        response_2 = self.datetime_facade.get_all_days_with_weekday_filters_for_this_month(weekdays=[0, 1])
        print(f"Filtered November 2024: {response_2}\n")

        # First Day of the month
        self.datetime_facade.set_datetime_to_first_day_of_current_month()
        response = self.datetime_facade.get_all_days_for_this_month()
        print(f"First day of current month: {response}\n")
        response_2 = self.datetime_facade.get_all_days_with_weekday_filters_for_this_month(weekdays=[0, 1])
        print(f"Filtered First day of current month: {response_2}\n")

        # Back to current day
        self.datetime_facade.set_datetime_to_current_day()
        response = self.datetime_facade.get_all_days_for_this_month()
        print(f"back to current: {response}\n")
        response_2 = self.datetime_facade.get_all_days_with_weekday_filters_for_this_month(weekdays=[0, 1])
        print(f"Filtered back to current: {response_2}\n")

    def test_get_all_time_within_a_span(self):
        # Default
        print(f"START TIME: {self.time_facade.start_time}")
        print(f"END TIME: {self.time_facade.end_time}")

        # Using Integeres
        self.time_facade.set_start_time_using_integers(hour=10, minute=30)
        self.time_facade.set_end_time_using_integers(hour=22, minute=30)
        print(f"START TIME 2: {self.time_facade.start_time}")
        print(f"END TIME 2: {self.time_facade.end_time}")
        all_time_within_a_span = self.time_facade.get_all_time_from_start_to_end_range()
        all_time_within_a_span_string = DateTimeFormatters.convert_datetime_to_time_string(all_time_within_a_span)
        print(f"ALL using Integers: {all_time_within_a_span_string}")

        # Using Strings
        start_time = '10:00 AM'
        end_time = '01:00 PM'
        self.time_facade.set_start_time_using_strings(start_time)
        self.time_facade.set_end_time_using_strings(end_time)
        all_time_within_a_span_using_strings = self.time_facade.get_all_time_from_start_to_end_range()
        all_time_within_a_span_using_strings_string = DateTimeFormatters.convert_datetime_to_time_string(all_time_within_a_span_using_strings)
        print(f"ALL using Strings: {all_time_within_a_span_using_strings_string}")

    def test_filter_time_slots(self):
        # Default 8AM to 8PM
        time_slots = self.time_facade.get_all_time_from_start_to_end_range()
        # Default 8AM to 8PM - Filter Existing Time Slots
        print(f"Time Slots:\n{DateTimeFormatters.convert_datetime_to_time_string(time_slots)}")
        existing_time_slots = [
            {
                "start_time": self.time_facade.create_time_object_with_integers(13, 0),
                "duration": 45,
                "has_processing_time": False,
                "application_time": 15,
                "processing_time": 15,
                "finishing_time": 15
            },
            {
                "start_time": self.time_facade.create_time_object_with_integers(15, 0),
                "duration": 60,
                "has_processing_time": True,
                "application_time": 15,
                "processing_time": 30,
                "finishing_time": 15
            },
            {
                "start_time": self.time_facade.create_time_object_with_integers(15, 30),
                "duration": 15,
                "has_processing_time": False,
                "application_time": 15,
                "processing_time": 30,
                "finishing_time": 15
            }
        ]
        time_slots_existing_slot_filters = self.time_facade.get_all_time_from_start_to_end_with_existing_time_filters(existing_time_slots)
        print(f"Filtered existing time slots:\n{DateTimeFormatters.convert_datetime_to_time_string(time_slots_existing_slot_filters)}\n")

        # Adjust 10AM to 10PM
        self.time_facade.set_start_time_using_integers(10, 0)
        self.time_facade.set_end_time_using_integers(22, 0)
        time_slots = self.time_facade.get_all_time_from_start_to_end_range()
        print(f"Time Slots:\n{DateTimeFormatters.convert_datetime_to_time_string(time_slots)}")
        # Adjust 10AM to 4PM - Filter Existing Time Slots
        time_slots_existing_slot_filters = self.time_facade.get_all_time_from_start_to_end_with_existing_time_filters(existing_time_slots)
        print(f"Filtered existing time slots:\n{DateTimeFormatters.convert_datetime_to_time_string(time_slots_existing_slot_filters)}\n")
        # Adjust 10AM to 4PM - Filter again with service duration
        time_slots_service_filter = self.time_facade.get_all_time_from_start_to_end_with_service_filters(60)
        print(f"Filtered service time slots:\n{DateTimeFormatters.convert_datetime_to_time_string(time_slots_service_filter)}\n")
        # Adjust 10AM to 4PM - Filter again with optimized booking
        time_slots_optimised_filters = self.time_facade.get_all_time_from_start_to_end_with_optimized_filters(30)
        print(f"Filtered optimized slots:\n{DateTimeFormatters.convert_datetime_to_time_string(time_slots_optimised_filters)}\n")
