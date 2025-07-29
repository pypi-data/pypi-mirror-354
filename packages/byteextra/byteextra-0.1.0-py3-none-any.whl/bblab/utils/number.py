"""Utility of numbers."""

from datetime import datetime

# fmt: off
ones = {
    0: '', 1: 'one', 2: 'two', 3: 'three', 4: 'four', 5: 'five', 6: 'six',
    7: 'seven', 8: 'eight', 9: 'nine', 10: 'ten', 11: 'eleven', 12: 'twelve',
    13: 'thirteen', 14: 'fourteen', 15: 'fifteen', 16: 'sixteen',
    17: 'seventeen', 18: 'eighteen', 19: 'nineteen'}
tens = {
    2: 'twenty', 3: 'thirty', 4: 'forty', 5: 'fifty', 6: 'sixty',
    7: 'seventy', 8: 'eighty', 9: 'ninety'}
illions = {
    1: 'thousand', 2: 'million', 3: 'billion', 4: 'trillion', 5: 'quadrillion',
    6: 'quintillion', 7: 'sextillion', 8: 'septillion', 9: 'octillion',
    10: 'nonillion', 11: 'decillion'}

# fmt: on
def num_to_word(i: int) -> str:
    """
    Convert an integer in to it's word representation.

    say_number(i: integer) -> string
    """
    if i < 0:
        return _join("negative", _say_number_pos(-i))
    if i == 0:
        return "zero"
    return _say_number_pos(i)


"""ordinal = lambda n: "%d%s" % (n,"tsnrhtdd"[(n//10%10!=1)*(n%10<4)*n%10::4])"""


def ordinal(n: int) -> str:
    """Get ordinal representation of an integer."""
    suffix = "th" if 11 <= n % 100 <= 13 else ["th", "st", "nd", "rd", "th"][min(n % 10, 4)]
    return str(n) + suffix


def commaify(num: int) -> str:
    """Adds commas to integer like accounting format."""
    new_number = ""
    for i, n in enumerate(str(num)[::-1]):
        if i and not i % 3:
            new_number += ","
        new_number += n
    return new_number[::-1]


def human_format(num: int, factor: int = 1000, *, long_suffix: bool = False):
    """Number (integer) to Kilo, Mega, Giga, Tera suffixed."""
    if num is None:
        num = 0
    magnitude = 0
    while abs(num) >= factor:
        magnitude += 1
        num /= factor * 1.0
    if not magnitude:
        return num
    return f"{num:.2f}{['', 'K', 'M', 'G', 'T', 'P'][magnitude]}{'iB' if long_suffix else ''}"


num_to_KMGTP = num_to_kilo_mega_giga = human_format


def bytes_to_KMGTP(num: int, factor: int = 1024):
    """Number (integer) to Kilo, Mega, Giga, Tera suffixed."""
    if num is None:
        num = 0
    magnitude = 0
    while abs(num) >= factor:
        magnitude += 1
        num /= factor * 1.0
    if not magnitude:
        return num
    return f"{num:.2f}{['', 'KB', 'MB', 'GB', 'TB', 'PB'][magnitude]}"


def human_time(
    value: float | datetime,
    *,
    spaced: bool = False,
    capitalized: bool = False,
    long_suffix: bool = False,
) -> str:
    """From total seconds or a datetime obj get human-readable time difference.

    :param value: total seconds or a datetime object.
    :param spaced: whether to add a space between numerical part and text/letter suffix.
    :param capitalized: whether to convert the text part first letter in title case.
    :param long_suffix: whether to have long suffix like years, months, days...
    :return: str (ex: 5 years 3 months 1 day 8 hours 9 minutes 12 seconds)
    """
    if isinstance(value, datetime):
        value = abs((datetime.now() - value).total_seconds())  # noqa: DTZ005
    total_seconds = int(value)

    # Define time units
    seconds_in_minute = 60
    seconds_in_hour = 60 * seconds_in_minute
    seconds_in_day = 24 * seconds_in_hour
    seconds_in_year = int(365.25 * seconds_in_day)
    seconds_in_month = int(30.44 * seconds_in_day)  # average month duration

    # Break down total_seconds
    years, remainder = divmod(total_seconds, seconds_in_year)
    months, remainder = divmod(remainder, seconds_in_month)
    days, remainder = divmod(remainder, seconds_in_day)
    hours, remainder = divmod(remainder, seconds_in_hour)
    minutes, seconds = divmod(remainder, seconds_in_minute)

    _s = {
        "y": "year" if long_suffix else "y",
        "m": "month" if long_suffix else "mo",
        "d": "day" if long_suffix else "d",
        "H": "hour" if long_suffix else "h",
        "M": "minute" if long_suffix else "m",
        "S": "second" if long_suffix else "s",
    }

    if capitalized or spaced:
        for k in list(_s.keys()):
            _s[k] = (" " if spaced else "") + (_s[k].title() if capitalized else _s[k])

    parts = []
    if years:
        parts.append(f"{years}{_s['y']}{'s' if long_suffix and years > 1 else ''}")
    if months:
        parts.append(f"{months}{_s['m']}{'s' if long_suffix and months > 1 else ''}")
    if days:
        parts.append(f"{days}{_s['d']}{'s' if long_suffix and days > 1 else ''}")
    if hours:
        parts.append(f"{hours}{_s['H']}{'s' if long_suffix and hours > 1 else ''}")
    if minutes:
        parts.append(f"{minutes}{_s['M']}{'s' if long_suffix and minutes > 1 else ''}")
    if not parts or seconds:
        parts.append(f"{seconds}{_s['S']}{'s' if long_suffix and seconds > 1 else ''}")

    return " ".join(parts)


def human_time_countdown(total_seconds):
    """Total seconds formatted like a countdown clock."""
    total_seconds = int(total_seconds)
    days, remainder = divmod(total_seconds, 60 * 60 * 24)
    hours, remainder = divmod(remainder, 60 * 60)
    minutes, seconds = divmod(remainder, 60)

    text = ""
    text += f"{days:02d}:" if days else ""
    # if days:return text
    text += f"{hours:02d}:" if hours else ""
    text += f"{minutes:02d}:" if minutes else ""
    # if hours:return text
    text += f"{seconds:02d}"
    return text


# ruff: noqa: PLR2004
def _say_number_pos(i):
    if i < 20:
        return ones[i]
    if i < 100:
        return _join(tens[i // 10], ones[i % 10])
    if i < 1000:
        return _divide(i, 100, "hundred")
    illions_number, illions_name = 1, illions[1]
    for illions_number, illions_name in illions.items():  # noqa: B007
        if i < 1000 ** (illions_number + 1):
            break
    return _divide(i, 1000**illions_number, illions_name)


def _divide(dividend, divisor, magnitude):
    return _join(
        _say_number_pos(dividend // divisor),
        magnitude,
        _say_number_pos(dividend % divisor),
    )


def _join(*args):
    return " ".join(filter(bool, args))
