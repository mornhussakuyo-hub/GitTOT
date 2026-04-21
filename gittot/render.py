import csv
import json
import sys

from gittot.stats import summarize_buckets


def render_chart(buckets, group_by, max_bar_width=25):
    RED = "\033[31m"
    GREEN = "\033[32m"
    RESET = "\033[0m"

    totals = summarize_buckets(buckets)
    max_value = max((max(bucket["add"], bucket["del"]) for bucket in buckets), default=0)
    if max_value == 0:
        max_value = 1

    label_width = max((len(bucket["bucket"]) for bucket in buckets), default=6)

    print("=" * 86)
    print(
        f"Code Change Distribution by {group_by} "
        f"(Commits: {totals['commits']}, Added: +{totals['add']}, Deleted: -{totals['del']})"
    )
    print("Note: commit timestamps are shown in your machine's local time zone.")
    print("Legend: left is deletions (-), center is the zero axis, and right is additions (+).")
    print()

    for bucket in buckets:
        add_val = bucket["add"]
        del_val = bucket["del"]
        add_len = int(add_val / max_value * max_bar_width)
        del_len = int(del_val / max_value * max_bar_width)

        left = " " * (max_bar_width - del_len) + RED + "█" * del_len + RESET
        right = GREEN + "█" * add_len + RESET + " " * (max_bar_width - add_len)

        print(
            f"{bucket['bucket']:<{label_width}} |{left}│{right}| "
            f"-{del_val} / +{add_val} ({bucket['commits']} commits)"
        )

    print("=" * 86)


def render_json(buckets, group_by):
    payload = {
        "group_by": group_by,
        "totals": summarize_buckets(buckets),
        "rows": buckets,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


def render_csv(buckets):
    writer = csv.DictWriter(sys.stdout, fieldnames=["bucket", "add", "del", "commits"])
    writer.writeheader()
    writer.writerows(buckets)


def render_output(buckets, group_by, output_format):
    if output_format == "chart":
        render_chart(buckets, group_by)
        return

    if output_format == "json":
        render_json(buckets, group_by)
        return

    if output_format == "csv":
        render_csv(buckets)
        return

    raise ValueError(f"Unsupported output format: {output_format}")
