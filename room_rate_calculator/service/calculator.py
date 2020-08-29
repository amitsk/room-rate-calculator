from datetime import date, timedelta
from room_rate_calculator.service.api import get_public_holidays, Holiday


def room_rate(base_rate: float, stay_date: date) -> float:
    room_rate = base_rate
    total_adjustment = (
        _weekend_adjustment(stay_date)
        + _public_holiday_adjustment(stay_date)
        + _month_adjustment(stay_date)
    )
    room_rate = room_rate + base_rate * total_adjustment

    return room_rate


def _weekend_adjustment(dt: date) -> float:
    day_of_week = dt.isoweekday()
    if day_of_week == 5 or day_of_week == 6:
        return 1.2
    return 1.0


# [{'2020-01-01', "New Year's Day"}, {'2020-01-20', 'Martin Luther King, Jr. Day'}]
def _public_holiday_adjustment(dt: date) -> float:
    """
    Get adjustment for a Public Holiday. If the next day is holiday, apply adjustment

    Args:
        dt (date): date from which to apply adjustment

    Returns:
        float: adjustment factor : 1.0 by default
    """
    holidays = get_public_holidays(dt)

    if any(
        [itm.date == (dt + timedelta(days=1)).strftime("%Y-%m-%d") for itm in holidays]
    ):
        return 0.2
    return 0.0


def _month_adjustment(dt: date) -> float:
    month = date.month
    if month in [6, 7, 8]:
        return 0.30
    elif month in [10, 11, 1, 2, 3]:
        return -0.20
    elif month == 12:
        return 0.10

    return 0.0