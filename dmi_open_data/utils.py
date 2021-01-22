from datetime import datetime


EPOCH = datetime.utcfromtimestamp(0)


def date2microseconds(date: datetime) -> int:
    return int((date - EPOCH).total_seconds() * 1000000.0)


def microseconds2date(microseconds: float) -> datetime:
    return datetime.utcfromtimestamp(microseconds / 1000000)
