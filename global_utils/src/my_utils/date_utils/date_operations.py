from datetime import datetime, timedelta
import calendar
from typing import List, Tuple


class DateFacade:

    def __init__(self) -> None:
        """
        When instantiated, it will set to current year and month.
        """
        self._datetime_operations = DateOperations
        self._date_filteres = DateFilters
        self._current_datetime = self._datetime_operations.get_current_datetime()
        self.year = self._current_datetime.year
        self.month = self._current_datetime.month

    def _get_all_days_for_this_month_process(self) -> List[datetime]:
        start_dt, end_dt = self._datetime_operations.get_start_and_end_date_of_month(self._current_datetime)
        return self._datetime_operations.get_all_days_within_a_span(start_dt, end_dt)

    def _update_datetime_details(self) -> None:
        self.year = self._current_datetime.year
        self.month = self._current_datetime.month

    def set_datetime_using_integers(self, year: int, month: int, day: int = 1) -> None:
        self._current_datetime = self._datetime_operations.get_datetime_using_integers(year, month, day)
        self._update_datetime_details()

    def set_datetime_to_current_day(self) -> None:
        self._current_datetime = self._datetime_operations.get_current_datetime()
        self._update_datetime_details()

    def set_datetime_to_first_day_of_current_month(self) -> None:
        self._current_datetime = self._datetime_operations.get_first_datetime_of_the_current_month()
        self._update_datetime_details()

    def get_current_datetime(self) -> datetime:
        return self._current_datetime

    def get_all_days_for_this_month(self) -> List[datetime]:
        return self._get_all_days_for_this_month_process()

    def get_all_days_with_weekday_filters_for_this_month(self, weekdays: List[int]) -> List[datetime]:
        all_days_for_this_month = self._get_all_days_for_this_month_process()
        return self._date_filteres.filter_dates_by_weekdays(all_days_for_this_month, weekdays)


class DateOperations:

    @staticmethod
    def adjust_year_and_month(year: int, month: int) -> Tuple[int, int]:
        year += (month - 1) // 12  # Floor Division
        if month % 12 == 0:
            month = 12
        else:
            month = month % 12
        return year, month

    @staticmethod
    def get_current_datetime() -> datetime:
        return datetime.now()

    @staticmethod
    def get_first_datetime_of_the_current_month() -> datetime:
        current_dt = datetime.now()
        return datetime(year=current_dt.year, month=current_dt.month, day=1)

    @staticmethod
    def get_datetime_using_integers(year: int, month: int, day: int = 1) -> datetime:
        year, month = DateOperations.adjust_year_and_month(year, month)
        return datetime(year=year, month=month, day=day)

    @staticmethod
    def get_start_and_end_date_of_month(dt_obj: datetime) -> Tuple[datetime, datetime]:
        last_day = calendar.monthrange(dt_obj.year, dt_obj.month)[1]
        end_date = datetime(dt_obj.year, dt_obj.month, last_day)
        return dt_obj, end_date

    @staticmethod
    def get_all_days_within_a_span(start_date: datetime, end_date: datetime) -> List[datetime]:
        current_date = start_date
        dates = []
        while current_date <= end_date:
            dates.append(current_date)
            current_date += timedelta(days=1)
        return dates


class DateFilters:

    @staticmethod
    def filter_dates_by_weekdays(dates: List[datetime], weekdays: List[int]) -> List[datetime]:
        return [date for date in dates if date.weekday() in weekdays]
