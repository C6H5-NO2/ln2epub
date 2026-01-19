from datetime import UTC, datetime


def datetime_iso8601(t: datetime = None) -> str:
    if t is None:
        t = datetime.now(UTC)
    else:
        t = datetime.fromtimestamp(t.timestamp(), tz=UTC)
    return t.isoformat(sep='T', timespec='seconds').replace('+00:00', 'Z')
