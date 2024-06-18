from datetime import datetime, timedelta
from typing import List


class DateTimeFormatters:
    @staticmethod
    def convert_datetime_to_datetime_string_web_online_format(dates: List[datetime]) -> List[str]:
        return [date.strftime('%A, %B %d, %Y').replace(" 0", " ") for date in dates]

    @staticmethod
    def convert_datetime_to_datetime_string(dates: List[datetime]) -> List[str]:
        return [date.strftime("%Y-%m-%d %H:%M") for date in dates]

    @staticmethod
    def convert_datime_to_date_string(dates: List[datetime]) -> List[str]:
        return [date.strftime("%Y-%m-%d") for date in dates]

    @staticmethod
    def convert_datetime_to_time_string(string_times: List[datetime]) -> List[str]:
        return [string_time.strftime("%I:%M %p") for string_time in string_times]

    @staticmethod
    def convert_time_string_to_datetime(string_times: List[str]) -> List[datetime]:
        return [datetime.strptime(string_time, "%I:%M %p") for string_time in string_times]

    @staticmethod
    def combine_date_and_time(date: str, time: str) -> datetime:
        date_time_str = f"{date} {time}"
        return datetime.strptime(date_time_str, "%B %d, %Y %H:%M")

    @staticmethod
    def combine_datetime_obj_and_time(date_obj: datetime, time_str: str) -> datetime:
        time_obj = datetime.strptime(time_str, '%I:%M %p').time()
        combined_datetime = datetime.combine(date_obj.date(), time_obj)
        return combined_datetime

    @staticmethod
    def combine_date_and_time_with_weekday(date: str, time: str) -> datetime:
        date_time_str = f"{date} {time}"
        return datetime.strptime(date_time_str, "%A, %B %d, %Y %H:%M")


class TimezoneConverter:
    """
    datetime native timezone is None.
    When sent to the server, it converts it to GMT format.
    When displayed back to the frontend, it will adjust to the selected timezone of the profile.
    This class adjusts the timezone before sending it to the server.
    """
    perth_au = 8
    darwin_au = 9.5
    sydney_au = 10

    @staticmethod
    def convert_to_perth_australia(dt_obj: datetime) -> datetime:
        return dt_obj - timedelta(hours=TimezoneConverter.perth_au)

    @staticmethod
    def convert_to_darwin_australia(dt_obj: datetime) -> datetime:
        return dt_obj - timedelta(hours=TimezoneConverter.darwin_au)

    @staticmethod
    def convert_to_sydney_australia(dt_obj: datetime) -> datetime:
        return dt_obj - timedelta(hours=TimezoneConverter.sydney_au)
