from collections import defaultdict
from datetime import datetime


GROUP_BY_CHOICES = ("hour", "weekday", "date", "month")
WEEKDAY_LABELS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")


def _empty_bucket(label):
    return {"bucket": label, "add": 0, "del": 0, "commits": 0}


def _build_bucket_label(timestamp: int, group_by: str) -> str:
    dt = datetime.fromtimestamp(timestamp)

    if group_by == "hour":
        return f"{dt.hour:02d}:00"
    if group_by == "weekday":
        return WEEKDAY_LABELS[dt.weekday()]
    if group_by == "date":
        return dt.strftime("%Y-%m-%d")
    if group_by == "month":
        return dt.strftime("%Y-%m")

    raise ValueError(f"Unsupported grouping: {group_by}")


def group_commits(commits, group_by="hour"):
    if group_by not in GROUP_BY_CHOICES:
        raise ValueError(f"Unsupported grouping: {group_by}")

    if group_by == "hour":
        ordered_labels = [f"{hour:02d}:00" for hour in range(24)]
        grouped = {label: _empty_bucket(label) for label in ordered_labels}
    elif group_by == "weekday":
        ordered_labels = list(WEEKDAY_LABELS)
        grouped = {label: _empty_bucket(label) for label in ordered_labels}
    else:
        ordered_labels = None
        grouped = defaultdict(lambda: None)

    for commit in commits:
        label = _build_bucket_label(commit["timestamp"], group_by)
        if label not in grouped or grouped[label] is None:
            grouped[label] = _empty_bucket(label)

        grouped[label]["add"] += commit["add"]
        grouped[label]["del"] += commit["del"]
        grouped[label]["commits"] += 1

    if ordered_labels is not None:
        return [grouped[label] for label in ordered_labels]

    return [grouped[label] for label in sorted(grouped)]


def summarize_buckets(buckets):
    return {
        "add": sum(bucket["add"] for bucket in buckets),
        "del": sum(bucket["del"] for bucket in buckets),
        "commits": sum(bucket["commits"] for bucket in buckets),
    }


def group_by_hour(commits):
    hour_buckets = group_commits(commits, group_by="hour")
    return {
        index: {
            "add": bucket["add"],
            "del": bucket["del"],
            "commits": bucket["commits"],
        }
        for index, bucket in enumerate(hour_buckets)
    }
