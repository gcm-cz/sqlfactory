"""Date/Time SQL functions (https://mariadb.com/kb/en/date-time-functions/)."""
from typing import Any, Literal

from .base import Function
from .. import StatementWithArgs, Statement, Raw


# pylint: disable=too-many-instance-attributes
class Interval(StatementWithArgs):
    """
    INTERVAL statement for DATE_ADD, DATE_SUB and similar functions.
    """
    _ATTRIBUTES = (
        "microsecond", "second", "minute", "hour", "day", "week", "month", "quarter", "year",
        "second_microsecond", "minute_microsecond", "minute_second", "hour_microsecond", "hour_second",
        "hour_minute", "day_microsecond", "day_second", "day_minute", "day_hour", "year_month"
    )

    # pylint: disable=too-many-arguments, too-many-locals
    def __init__(
            self,
            microsecond: Any = None,
            second: Any = None,
            minute: Any = None,
            hour: Any = None,
            day: Any = None,
            week: Any = None,
            month: Any = None,
            quarter: Any = None,
            year: Any = None,
            second_microsecond: Any = None,
            minute_microsecond: Any = None,
            minute_second: Any = None,
            hour_microsecond: Any = None,
            hour_second: Any = None,
            hour_minute: Any = None,
            day_microsecond: Any = None,
            day_second: Any = None,
            day_minute: Any = None,
            day_hour: Any = None,
            year_month: Any = None
    ):
        self.microsecond = microsecond
        self.second = second
        self.minute = minute
        self.hour = hour
        self.day = day
        self.week = week
        self.month = month
        self.quarter = quarter
        self.year = year
        self.second_microsecond = second_microsecond
        self.minute_microsecond = minute_microsecond
        self.minute_second = minute_second
        self.hour_microsecond = hour_microsecond
        self.hour_second = hour_second
        self.hour_minute = hour_minute
        self.day_microsecond = day_microsecond
        self.day_second = day_second
        self.day_minute = day_minute
        self.day_hour = day_hour
        self.year_month = year_month

        if all(getattr(self, attr) is None for attr in self._ATTRIBUTES):
            raise ValueError("At least one attribute must be set.")

    def __str__(self):
        return "INTERVAL " + " ".join(
            f"{'%s' if not isinstance(getattr(self, attr), Statement) else str(getattr(self, attr))} {attr.upper()}"
            for attr in reversed(self._ATTRIBUTES)
            if getattr(self, attr) is not None
        )

    @property
    def args(self) -> list[Any]:
        args = []

        for attr in reversed(self._ATTRIBUTES):
            value = getattr(self, attr)
            if value is None:
                continue

            if isinstance(value, StatementWithArgs):
                args.extend(value.args)

            elif not isinstance(value, Statement):
                args.append(value)

        return args


# pylint: disable=too-few-public-methods
class AddMonths(Function):
    """
    Adds months to date.
    """
    def __init__(self, date: Any, months: int):
        super().__init__("ADDMONTHS", date, months)


# pylint: disable=too-few-public-methods
class AddDate(Function):
    """
    Adds days to date.
    """
    def __init__(self, date: Any, days: int | Interval):
        super().__init__("ADDDATE", date, days)


# pylint: disable=too-few-public-methods
class AddTime(Function):
    """
    Adds time to date.
    """
    def __init__(self, date: Any, time: Any):
        super().__init__("ADDTIME", date, time)


# pylint: disable=too-few-public-methods
class ConvertTz(Function):
    """
    Converts date from one timezone to another.
    """
    def __init__(self, date: Any, from_tz: str, to_tz: str):
        super().__init__("CONVERT_TZ", date, from_tz, to_tz)


# pylint: disable=too-few-public-methods
class CurDate(Function):
    """
    Returns current date.
    """
    def __init__(self):
        super().__init__("CURDATE")


# pylint: disable=too-few-public-methods
class CurrentDate(Function):
    """
    Returns current date.
    """
    def __init__(self):
        super().__init__("CURRENT_DATE")


# pylint: disable=too-few-public-methods
class CurrentTime(Function):
    """
    Returns current time.
    """
    def __init__(self):
        super().__init__("CURRENT_TIME")


# pylint: disable=too-few-public-methods
class CurrentTimestamp(Function):
    """
    Returns current timestamp.
    """
    def __init__(self):
        super().__init__("CURRENT_TIMESTAMP")


# pylint: disable=too-few-public-methods
class CurTime(Function):
    """
    Returns current time.
    """
    def __init__(self):
        super().__init__("CURTIME")


# pylint: disable=too-few-public-methods
class Date(Function):
    """
    Extracts date from datetime.
    """
    def __init__(self, date: Any):
        super().__init__("DATE", date)


# pylint: disable=too-few-public-methods
class DateDiff(Function):
    """
    Returns difference between two dates.
    """
    def __init__(self, date1: Any, date2: Any):
        super().__init__("DATEDIFF", date1, date2)


# pylint: disable=too-few-public-methods
class DateAdd(Function):
    """
    Adds interval to date.
    """
    def __init__(self, date: Any, interval: Interval):
        super().__init__("DATE_ADD", date, interval)


# pylint: disable=too-few-public-methods
class DateFormat(Function):
    """
    Formats date.
    """
    def __init__(self, date: Any, date_format: str):
        super().__init__("DATE_FORMAT", date, date_format)


# pylint: disable=too-few-public-methods
class DateSub(Function):
    """
    Subtracts interval from date.
    """
    def __init__(self, date: Any, interval: Interval):
        super().__init__("DATE_SUB", date, interval)


# pylint: disable=too-few-public-methods
class Day(Function):
    """
    Extracts day from date.
    """
    def __init__(self, date: Any):
        super().__init__("DAY", date)


# pylint: disable=too-few-public-methods
class DayName(Function):
    """
    Returns name of the day.
    """
    def __init__(self, date: Any):
        super().__init__("DAYNAME", date)


# pylint: disable=too-few-public-methods
class DayOfMonth(Function):
    """
    Extracts day of month from date.
    """
    def __init__(self, date: Any):
        super().__init__("DAYOFMONTH", date)


# pylint: disable=too-few-public-methods
class DayOfWeek(Function):
    """
    Extracts day of week from date.
    """
    def __init__(self, date: Any):
        super().__init__("DAYOFWEEK", date)


# pylint: disable=too-few-public-methods
class DayOfYear(Function):
    """
    Extracts day of year from date.
    """
    def __init__(self, date: Any):
        super().__init__("DAYOFYEAR", date)


# pylint: disable=too-few-public-methods
class Extract(Function):
    """
    Extracts part of date.
    """
    def __init__(self, unit: str, date: Any):
        args = [date] if not isinstance(date, Statement) else date.args if isinstance(date, StatementWithArgs) else []
        super().__init__(
            "EXTRACT",
            Raw(
                f"{unit} FROM {str(date) if isinstance(date, Statement) else '%s'}",
                *args
            )
        )


# pylint: disable=too-few-public-methods
class FormatPicoTime(Function):
    """
    Formats pico time.
    """
    def __init__(self, time: Any):
        super().__init__("FORMAT_PICO_TIME", time)


# pylint: disable=too-few-public-methods
class FromDays(Function):
    """
    Converts days to date.
    """
    def __init__(self, days: Any):
        super().__init__("FROM_DAYS", days)


# pylint: disable=too-few-public-methods
class FromUnixTime(Function):
    """
    Converts UNIX timestamp to date.
    """
    def __init__(self, unix_timestamp: Any):
        super().__init__("FROM_UNIXTIME", unix_timestamp)


# pylint: disable=too-few-public-methods
class GetFormat(Function):
    """
    Returns date format.
    """
    def __init__(
            self,
            date_format: Literal["DATE", "DATETIME", "TIME"],
            locale: Literal["EUR", "USA", "JIS", "ISO", "INTERNAL"]
    ):
        super().__init__("GET_FORMAT", Raw(date_format), locale)


# pylint: disable=too-few-public-methods
class Hour(Function):
    """
    Extracts hour from datetime.
    """
    def __init__(self, time: Any):
        super().__init__("HOUR", time)


# pylint: disable=too-few-public-methods
class LastDay(Function):
    """
    Returns last day of month.
    """
    def __init__(self, date: Any):
        super().__init__("LAST_DAY", date)


# pylint: disable=too-few-public-methods
class LocalTime(Function):
    """
    Returns local time.
    """
    def __init__(self):
        super().__init__("LOCALTIME")


# pylint: disable=too-few-public-methods
class LocalTimestamp(Function):
    """
    Returns local timestamp.
    """
    def __init__(self):
        super().__init__("LOCALTIMESTAMP")


# pylint: disable=too-few-public-methods
class MakeDate(Function):
    """
    Creates date from year and day of year.
    """
    def __init__(self, year: Any, day_of_year: Any):
        super().__init__("MAKEDATE", year, day_of_year)


# pylint: disable=too-few-public-methods
class MakeTime(Function):
    """
    Creates time from hours, minutes, seconds.
    """
    def __init__(self, hours: Any, minutes: Any, seconds: Any):
        super().__init__("MAKETIME", hours, minutes, seconds)


# pylint: disable=too-few-public-methods
class Microsecond(Function):
    """
    Extracts microseconds from datetime.
    """
    def __init__(self, time: Any):
        super().__init__("MICROSECOND", time)


# pylint: disable=too-few-public-methods
class Minute(Function):
    """
    Extracts minutes from datetime.
    """
    def __init__(self, time: Any):
        super().__init__("MINUTE", time)


# pylint: disable=too-few-public-methods
class MonthName(Function):
    """
    Returns name of the month.
    """
    def __init__(self, date: Any):
        super().__init__("MONTHNAME", date)


# pylint: disable=too-few-public-methods
class Now(Function):
    """
    Returns current date and time.
    """
    def __init__(self):
        super().__init__("NOW")


# pylint: disable=too-few-public-methods
class PeriodAdd(Function):
    """
    Add months to a period.
    """
    def __init__(self, date: Any, period: Any):
        super().__init__("PERIOD_ADD", date, period)


# pylint: disable=too-few-public-methods
class PeriodDiff(Function):
    """
    Returns number of months between two periods.
    """
    def __init__(self, period1: Any, period2: Any):
        super().__init__("PERIOD_DIFF", period1, period2)


# pylint: disable=too-few-public-methods
class Quarter(Function):
    """
    Extracts quarter from date.
    """
    def __init__(self, date: Any):
        super().__init__("QUARTER", date)


# pylint: disable=too-few-public-methods
class Second(Function):
    """
    Extracts seconds from datetime.
    """
    def __init__(self, time: Any):
        super().__init__("SECOND", time)


# pylint: disable=too-few-public-methods
class SecToTime(Function):
    """
    Converts seconds to time.
    """
    def __init__(self, seconds: Any):
        super().__init__("SEC_TO_TIME", seconds)


# pylint: disable=too-few-public-methods
class StrToDate(Function):
    """
    Converts string to date.
    """
    def __init__(self, date: Any, date_format: str):
        super().__init__("STR_TO_DATE", date, date_format)


# pylint: disable=too-few-public-methods
class SubDate(Function):
    """
    Subtracts days from date.
    """
    def __init__(self, date: Any, days: int | Interval):
        super().__init__("SUBDATE", date, days)


# pylint: disable=too-few-public-methods
class SubTime(Function):
    """
    Subtracts time from date.
    """
    def __init__(self, date: Any, time: Any):
        super().__init__("SUBTIME", date, time)


# pylint: disable=too-few-public-methods
class SysDate(Function):
    """
    Returns current date.
    """
    def __init__(self):
        super().__init__("SYSDATE")


# pylint: disable=too-few-public-methods
class Time(Function):
    """
    Extracts time from datetime.
    """
    def __init__(self, time: Any):
        super().__init__("TIME", time)



class TimeDiff(Function):
    """
    Returns difference between two times.
    """
    def __init__(self, time1: Any, time2: Any):
        super().__init__("TIMEDIFF", time1, time2)


# pylint: disable=too-few-public-methods
class Timestamp(Function):
    """
    Converts date to timestamp.
    """
    def __init__(self, date: Any):
        super().__init__("TIMESTAMP", date)


# pylint: disable=too-few-public-methods
class TimeFormat(Function):
    """
    Formats time.
    """
    def __init__(self, time: Any, date_format: str):
        super().__init__("TIME_FORMAT", time, date_format)


# pylint: disable=too-few-public-methods
class TimeToSec(Function):
    """
    Converts time to seconds.
    """
    def __init__(self, time: Any):
        super().__init__("TIME_TO_SEC", time)


# pylint: disable=too-few-public-methods
class ToDays(Function):
    """
    Converts date to days.
    """
    def __init__(self, date: Any):
        super().__init__("TO_DAYS", date)


# pylint: disable=too-few-public-methods
class ToSeconds(Function):
    """
    Converts date to seconds.
    """
    def __init__(self, date: Any):
        super().__init__("TO_SECONDS", date)


# pylint: disable=too-few-public-methods
class UnixTimestamp(Function):
    """
    Returns UNIX timestamp.
    """
    def __init__(self):
        super().__init__("UNIX_TIMESTAMP")


# pylint: disable=too-few-public-methods
class UtcDate(Function):
    """
    Returns current date in UTC.
    """
    def __init__(self):
        super().__init__("UTC_DATE")


# pylint: disable=too-few-public-methods
class UtcTime(Function):
    """
    Returns current time in UTC.
    """
    def __init__(self):
        super().__init__("UTC_TIME")


# pylint: disable=too-few-public-methods
class UtcTimestamp(Function):
    """
    Returns current timestamp in UTC.
    """
    def __init__(self):
        super().__init__("UTC_TIMESTAMP")


# pylint: disable=too-few-public-methods
class Week(Function):
    """
    Returns week number.
    """
    def __init__(self, date: Any, mode: int | Statement = None):
        if mode is not None:
            super().__init__("WEEK", date, mode)
        else:
            super().__init__("WEEK", date)


# pylint: disable=too-few-public-methods
class WeekDay(Function):
    """
    Returns day of week.
    """
    def __init__(self, date: Any):
        super().__init__("WEEKDAY", date)


# pylint: disable=too-few-public-methods
class WeekOfYear(Function):
    """
    Returns week of year.
    """
    def __init__(self, date: Any):
        super().__init__("WEEKOFYEAR", date)


# pylint: disable=too-few-public-methods
class Year(Function):
    """
    Extracts year from date.
    """
    def __init__(self, date: Any):
        super().__init__("YEAR", date)


# pylint: disable=too-few-public-methods
class YearWeek(Function):
    """
    Returns year and week number.
    """
    def __init__(self, date: Any, mode: int | Statement = None):
        if mode is None:
            super().__init__("YEARWEEK", date)
        else:
            super().__init__("YEARWEEK", date, mode)
