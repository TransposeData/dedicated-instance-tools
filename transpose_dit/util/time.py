from datetime import datetime, timezone

from dateutil import parser


def to_ts(timestmap_str: str) -> str:
    """
    Convert a timestamp string to a millisecond-timestamp integer.

    :param timestamp_str: The timestamp string.
    :return: The millisecond-timestamp integer.
    """

    dt = parser.parse(timestmap_str)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.astimezone(timezone.utc).replace(second=0).timestamp()) * 1000


def to_iso(dt: datetime) -> str:
    """
    Convert a datetime object to an ISO 8601 string.

    :param dt: The datetime object.
    :return: The ISO 8601 string.
    """

    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def estimate_eta(dt: datetime, synced: int, remaining: int) -> str:
    """
    Estimates the time remaining until a process is complete.

    :param dt: The datetime of when the process began.
    :param synced: The number of objs that have been completed.
    :param remaining: The number of objects remaining to be completed.
    :return: A string representing the estimated time remaining.
    """

    contracts_per_second = synced / (datetime.now() - dt).total_seconds()
    if contracts_per_second == 0:
        return "--"
    return __format_eta(int(remaining / contracts_per_second))


def __format_eta(seconds: int) -> str:
    """
    Format a time in seconds to a human readable string.

    :param seconds: The time in seconds.
    :return: The human readable string.
    """

    if seconds < 0:
        seconds = 0
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

    if d > 0:
        return "{:03.0f}d, {:02.0f}h, {:02.0f}m, {:02.0f}s".format(d, h, m, s)
    if h > 0:
        return "{:02.0f}h, {:02.0f}m, {:02.0f}s".format(h, m, s)
    if m > 0:
        return "{:02.0f}m, {:02.0f}s".format(m, s)
    return "{:02.0f}s".format(s)
