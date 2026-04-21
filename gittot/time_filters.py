from datetime import datetime


LOCAL_TIMEZONE = datetime.now().astimezone().tzinfo


def _looks_like_date_only(value: str) -> bool:
    return "T" not in value and " " not in value and ":" not in value


def parse_time_filter(value: str, end_of_day: bool = False) -> datetime:
    text = value.strip()
    if not text:
        raise ValueError("Time filter cannot be empty.")

    normalized = text[:-1] + "+00:00" if text.endswith("Z") else text

    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise ValueError(
            f"Invalid time filter: {value}. Use ISO-like formats such as 2026-04-01 or 2026-04-01T09:30:00+08:00."
        ) from exc

    if _looks_like_date_only(text):
        if end_of_day:
            parsed = parsed.replace(hour=23, minute=59, second=59, microsecond=0)
        else:
            parsed = parsed.replace(hour=0, minute=0, second=0, microsecond=0)

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=LOCAL_TIMEZONE)

    return parsed


def normalize_time_filter(value: str | None, end_of_day: bool = False) -> str | None:
    if value is None:
        return None

    return parse_time_filter(value, end_of_day=end_of_day).isoformat(timespec="seconds")


def normalize_time_filters(since: str | None, until: str | None) -> tuple[str | None, str | None]:
    normalized_since = normalize_time_filter(since, end_of_day=False)
    normalized_until = normalize_time_filter(until, end_of_day=True)

    if normalized_since and normalized_until:
        since_dt = parse_time_filter(normalized_since)
        until_dt = parse_time_filter(normalized_until)
        if since_dt > until_dt:
            raise ValueError("--since cannot be later than --until.")

    return normalized_since, normalized_until
