from collections import defaultdict
from datetime import datetime


def group_by_hour(commits):
    hour_stats = defaultdict(lambda: {"add": 0, "del": 0, "commits": 0})

    for commit in commits:
        hour = datetime.fromtimestamp(commit["timestamp"]).hour
        hour_stats[hour]["add"] += commit["add"]
        hour_stats[hour]["del"] += commit["del"]
        hour_stats[hour]["commits"] += 1

    return dict(sorted(hour_stats.items()))