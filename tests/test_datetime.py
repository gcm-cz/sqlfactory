import pytest

from sqlfactory import Column
from sqlfactory.func.control import IfNull
from sqlfactory.func.datetime import (
    AddDate,
    AddMonths,
    AddTime,
    ConvertTz,
    CurDate,
    CurrentDate,
    CurrentTime,
    CurrentTimestamp,
    CurTime,
    Date,
    DateAdd,
    DateDiff,
    DateFormat,
    DateSub,
    Day,
    DayName,
    DayOfMonth,
    DayOfWeek,
    DayOfYear,
    Extract,
    FormatPicoTime,
    FromDays,
    FromUnixTime,
    GetFormat,
    Hour,
    Interval,
    LastDay,
    LocalTime,
    LocalTimestamp,
    MakeDate,
    MakeTime,
    Microsecond,
    Minute,
    MonthName,
    Now,
    PeriodAdd,
    PeriodDiff,
    Quarter,
    Second,
    SecToTime,
    StrToDate,
    SubDate,
    SubTime,
    SysDate,
    Time,
    TimeDiff,
    TimeFormat,
    Timestamp,
    TimeToSec,
    ToDays,
    ToSeconds,
    UnixTimestamp,
    UtcDate,
    UtcTime,
    UtcTimestamp,
    Week,
    WeekDay,
    WeekOfYear,
    Year,
    YearWeek,
)


def test_interval():
    interval = Interval(day=5, hour=3)
    assert str(interval) == "INTERVAL %s DAY %s HOUR"
    assert interval.args == [5, 3]

    interval = Interval(year=2, month=1)
    assert str(interval) == "INTERVAL %s YEAR %s MONTH"
    assert interval.args == [2, 1]

    interval = Interval(minute=30, second=15)
    assert str(interval) == "INTERVAL %s MINUTE %s SECOND"
    assert interval.args == [30, 15]

    with pytest.raises(ValueError):
        Interval()

    interval = Interval(minute=Column("minute"))
    assert str(interval) == "INTERVAL `minute` MINUTE"
    assert interval.args == []


    interval = Interval(minute=IfNull(Column("minute"), 5))
    assert str(interval) == "INTERVAL IFNULL(`minute`, %s) MINUTE"
    assert interval.args == [5]


def test_add_months():
    add_months_func = AddMonths('2022-01-01', 1)
    assert str(add_months_func) == "ADDMONTHS(%s, %s)"
    assert add_months_func.args == ['2022-01-01', 1]


def test_add_date():
    add_date_func = AddDate('2022-01-01', 1)
    assert str(add_date_func) == "ADDDATE(%s, %s)"
    assert add_date_func.args == ['2022-01-01', 1]


def test_add_time():
    add_time_func = AddTime('01:00:00', '02:00:00')
    assert str(add_time_func) == "ADDTIME(%s, %s)"
    assert add_time_func.args == ['01:00:00', '02:00:00']


def test_convert_tz():
    convert_tz_func = ConvertTz('2022-01-01', 'UTC', 'Asia/Kolkata')
    assert str(convert_tz_func) == "CONVERT_TZ(%s, %s, %s)"
    assert convert_tz_func.args == ['2022-01-01', 'UTC', 'Asia/Kolkata']


def test_cur_date():
    cur_date_func = CurDate()
    assert str(cur_date_func) == "CURDATE()"
    assert cur_date_func.args == []


def test_current_date():
    current_date_func = CurrentDate()
    assert str(current_date_func) == "CURRENT_DATE()"
    assert current_date_func.args == []


def test_current_time():
    current_time_func = CurrentTime()
    assert str(current_time_func) == "CURRENT_TIME()"
    assert current_time_func.args == []


def test_current_timestamp():
    current_timestamp_func = CurrentTimestamp()
    assert str(current_timestamp_func) == "CURRENT_TIMESTAMP()"
    assert current_timestamp_func.args == []


def test_cur_time():
    cur_time_func = CurTime()
    assert str(cur_time_func) == "CURTIME()"
    assert cur_time_func.args == []


def test_date():
    date_func = Date('2022-01-01')
    assert str(date_func) == "DATE(%s)"
    assert date_func.args == ['2022-01-01']


def test_date_diff():
    date_diff_func = DateDiff('2022-01-01', '2022-01-02')
    assert str(date_diff_func) == "DATEDIFF(%s, %s)"
    assert date_diff_func.args == ['2022-01-01', '2022-01-02']


def test_date_add():
    date_add_func = DateAdd('2022-01-01', Interval(day=1))
    assert str(date_add_func) == "DATE_ADD(%s, INTERVAL %s DAY)"
    assert date_add_func.args == ['2022-01-01', 1]


def test_date_format():
    date_format_func = DateFormat('2022-01-01', '%Y-%m-%d')
    assert str(date_format_func) == "DATE_FORMAT(%s, %s)"
    assert date_format_func.args == ['2022-01-01', '%Y-%m-%d']


def test_date_sub():
    date_sub_func = DateSub('2022-01-01', Interval(day=1))
    assert str(date_sub_func) == "DATE_SUB(%s, INTERVAL %s DAY)"
    assert date_sub_func.args == ['2022-01-01', 1]


def test_day():
    day_func = Day('2022-01-01')
    assert str(day_func) == "DAY(%s)"
    assert day_func.args == ['2022-01-01']


def test_day_name():
    day_name_func = DayName('2022-01-01')
    assert str(day_name_func) == "DAYNAME(%s)"
    assert day_name_func.args == ['2022-01-01']


def test_day_of_month():
    day_of_month_func = DayOfMonth('2022-01-01')
    assert str(day_of_month_func) == "DAYOFMONTH(%s)"
    assert day_of_month_func.args == ['2022-01-01']


def test_day_of_week():
    day_of_week_func = DayOfWeek('2022-01-01')
    assert str(day_of_week_func) == "DAYOFWEEK(%s)"
    assert day_of_week_func.args == ['2022-01-01']


def test_day_of_year():
    day_of_year_func = DayOfYear('2022-01-01')
    assert str(day_of_year_func) == "DAYOFYEAR(%s)"
    assert day_of_year_func.args == ['2022-01-01']


def test_extract():
    extract_func = Extract('YEAR', '2022-01-01')
    assert str(extract_func) == "EXTRACT(YEAR FROM %s)"
    assert extract_func.args == ['2022-01-01']


def test_format_pico_time():
    format_pico_time_func = FormatPicoTime('01:00:00.123456789')
    assert str(format_pico_time_func) == "FORMAT_PICO_TIME(%s)"
    assert format_pico_time_func.args == ['01:00:00.123456789']


def test_from_days():
    from_days_func = FromDays(737791)
    assert str(from_days_func) == "FROM_DAYS(%s)"
    assert from_days_func.args == [737791]


def test_from_unix_time():
    from_unix_time_func = FromUnixTime(1640995200)
    assert str(from_unix_time_func) == "FROM_UNIXTIME(%s)"
    assert from_unix_time_func.args == [1640995200]


def test_get_format():
    get_format_func = GetFormat('DATE', 'EUR')
    assert str(get_format_func) == "GET_FORMAT(DATE, %s)"
    assert get_format_func.args == ['EUR']


def test_hour():
    hour_func = Hour('01:00:00')
    assert str(hour_func) == "HOUR(%s)"
    assert hour_func.args == ['01:00:00']


def test_last_day():
    last_day_func = LastDay('2022-01-01')
    assert str(last_day_func) == "LAST_DAY(%s)"
    assert last_day_func.args == ['2022-01-01']


def test_local_time():
    local_time_func = LocalTime()
    assert str(local_time_func) == "LOCALTIME()"
    assert local_time_func.args == []


def test_local_timestamp():
    local_timestamp_func = LocalTimestamp()
    assert str(local_timestamp_func) == "LOCALTIMESTAMP()"
    assert local_timestamp_func.args == []


def test_make_date():
    make_date_func = MakeDate(2022, 1)
    assert str(make_date_func) == "MAKEDATE(%s, %s)"
    assert make_date_func.args == [2022, 1]


def test_make_time():
    make_time_func = MakeTime(1, 0, 0)
    assert str(make_time_func) == "MAKETIME(%s, %s, %s)"
    assert make_time_func.args == [1, 0, 0]


def test_microsecond():
    microsecond_func = Microsecond('01:00:00.123456')
    assert str(microsecond_func) == "MICROSECOND(%s)"
    assert microsecond_func.args == ['01:00:00.123456']


def test_minute():
    minute_func = Minute('01:00:00')
    assert str(minute_func) == "MINUTE(%s)"
    assert minute_func.args == ['01:00:00']


def test_month_name():
    month_name_func = MonthName('2022-01-01')
    assert str(month_name_func) == "MONTHNAME(%s)"
    assert month_name_func.args == ['2022-01-01']


def test_now():
    now_func = Now()
    assert str(now_func) == "NOW()"
    assert now_func.args == []


def test_period_add():
    period_add_func = PeriodAdd(202201, 1)
    assert str(period_add_func) == "PERIOD_ADD(%s, %s)"
    assert period_add_func.args == [202201, 1]


def test_period_diff():
    period_diff_func = PeriodDiff(202201, 202202)
    assert str(period_diff_func) == "PERIOD_DIFF(%s, %s)"
    assert period_diff_func.args == [202201, 202202]


def test_quarter():
    quarter_func = Quarter('2022-01-01')
    assert str(quarter_func) == "QUARTER(%s)"
    assert quarter_func.args == ['2022-01-01']


def test_second():
    second_func = Second('01:00:00')
    assert str(second_func) == "SECOND(%s)"
    assert second_func.args == ['01:00:00']


def test_sec_to_time():
    sec_to_time_func = SecToTime(3600)
    assert str(sec_to_time_func) == "SEC_TO_TIME(%s)"
    assert sec_to_time_func.args == [3600]


def test_str_to_date():
    str_to_date_func = StrToDate('01,01,2022', '%d,%m,%Y')
    assert str(str_to_date_func) == "STR_TO_DATE(%s, %s)"
    assert str_to_date_func.args == ['01,01,2022', '%d,%m,%Y']


def test_sub_date():
    sub_date_func = SubDate('2022-01-01', Interval(day=1))
    assert str(sub_date_func) == "SUBDATE(%s, INTERVAL %s DAY)"
    assert sub_date_func.args == ['2022-01-01', 1]


def test_sub_time():
    sub_time_func = SubTime('01:00:00', '00:30:00')
    assert str(sub_time_func) == "SUBTIME(%s, %s)"
    assert sub_time_func.args == ['01:00:00', '00:30:00']


def test_sys_date():
    sys_date_func = SysDate()
    assert str(sys_date_func) == "SYSDATE()"
    assert sys_date_func.args == []


def test_time():
    time_func = Time('01:00:00')
    assert str(time_func) == "TIME(%s)"
    assert time_func.args == ['01:00:00']


def test_time_diff():
    time_diff_func = TimeDiff('02:00:00', '01:00:00')
    assert str(time_diff_func) == "TIMEDIFF(%s, %s)"
    assert time_diff_func.args == ['02:00:00', '01:00:00']


def test_timestamp():
    timestamp_func = Timestamp('2022-01-01 01:00:00')
    assert str(timestamp_func) == "TIMESTAMP(%s)"
    assert timestamp_func.args == ['2022-01-01 01:00:00']


def test_time_format():
    time_format_func = TimeFormat('01:00:00', '%H:%i:%s')
    assert str(time_format_func) == "TIME_FORMAT(%s, %s)"
    assert time_format_func.args == ['01:00:00', '%H:%i:%s']


def test_time_to_sec():
    time_to_sec_func = TimeToSec('01:00:00')
    assert str(time_to_sec_func) == "TIME_TO_SEC(%s)"
    assert time_to_sec_func.args == ['01:00:00']


def test_to_days():
    to_days_func = ToDays('2022-01-01')
    assert str(to_days_func) == "TO_DAYS(%s)"
    assert to_days_func.args == ['2022-01-01']


def test_to_seconds():
    to_seconds_func = ToSeconds('2022-01-01 01:00:00')
    assert str(to_seconds_func) == "TO_SECONDS(%s)"
    assert to_seconds_func.args == ['2022-01-01 01:00:00']


def test_unix_timestamp():
    unix_timestamp_func = UnixTimestamp()
    assert str(unix_timestamp_func) == "UNIX_TIMESTAMP()"
    assert unix_timestamp_func.args == []


def test_utc_date():
    utc_date_func = UtcDate()
    assert str(utc_date_func) == "UTC_DATE()"
    assert utc_date_func.args == []


def test_utc_time():
    utc_time_func = UtcTime()
    assert str(utc_time_func) == "UTC_TIME()"
    assert utc_time_func.args == []


def test_utc_timestamp():
    utc_timestamp_func = UtcTimestamp()
    assert str(utc_timestamp_func) == "UTC_TIMESTAMP()"
    assert utc_timestamp_func.args == []


def test_week():
    week_func = Week('2022-01-01', 1)
    assert str(week_func) == "WEEK(%s, %s)"
    assert week_func.args == ['2022-01-01', 1]

    week_func = Week("2022-01-01")
    assert str(week_func) == "WEEK(%s)"
    assert week_func.args == ["2022-01-01"]


def test_week_day():
    week_day_func = WeekDay('2022-01-01')
    assert str(week_day_func) == "WEEKDAY(%s)"
    assert week_day_func.args == ['2022-01-01']


def test_week_of_year():
    week_of_year_func = WeekOfYear('2022-01-01')
    assert str(week_of_year_func) == "WEEKOFYEAR(%s)"
    assert week_of_year_func.args == ['2022-01-01']


def test_year():
    year_func = Year('2022-01-01')
    assert str(year_func) == "YEAR(%s)"
    assert year_func.args == ['2022-01-01']


def test_year_week():
    year_week_func = YearWeek('2022-01-01', 1)
    assert str(year_week_func) == "YEARWEEK(%s, %s)"
    assert year_week_func.args == ['2022-01-01', 1]

    year_week_func = YearWeek("2022-01-01")
    assert str(year_week_func) == "YEARWEEK(%s)"
    assert year_week_func.args == ["2022-01-01"]
