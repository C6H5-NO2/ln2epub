from datetime import UTC, datetime


def datetime_iso8601(t: datetime = None) -> str:
    t = datetime.now(UTC) if t is None else datetime.fromtimestamp(t.timestamp(), tz=UTC)
    return t.isoformat(sep='T', timespec='seconds').replace('+00:00', 'Z')
