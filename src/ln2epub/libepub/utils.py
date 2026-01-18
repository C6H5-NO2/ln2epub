from datetime import datetime, UTC

_DATACLASS_KWARGS = dict(
    eq=False,
    order=False,
    frozen=True,
    match_args=False,
    kw_only=True,
)

_FIELD_KWARGS = dict(
    compare=False,
    kw_only=True,
)


def datetime_iso8601(t: datetime = None) -> str:
    t = datetime.now(UTC) if t is None else datetime.fromtimestamp(t.timestamp(), tz=UTC)
    return t.isoformat(sep='T', timespec='seconds').replace('+00:00', 'Z')
