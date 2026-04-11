def render_chart(hour_stats, max_bar_width=25):

    total_add = sum(v["add"] for v in hour_stats.values())
    total_del = sum(v["del"] for v in hour_stats.values())

    max_value = max(
        max(v["add"], v["del"]) for v in hour_stats.values()
    )
    if max_value == 0:
        max_value = 1

    print("=" * 70)
    print(f"Hourly Code Change Distribution (Total Added: +{total_add} lines, Total Deleted: -{total_del} lines)")
    print("Note: times have been automatically converted to your machine's local time zone.")
    print("Legend: left is deletions (-), center is the zero axis, and right is additions (+).")
    print()
    
    for hour in range(24):
        if hour_stats.get(hour) is None:
            add_val = 0
            del_val = 0
        else:
            add_val = hour_stats[hour]["add"]
            del_val = hour_stats[hour]["del"]


        add_len = int(add_val / max_value * max_bar_width)
        del_len = int(del_val / max_value * max_bar_width)

        left = " " * (max_bar_width - del_len) + "█" * del_len
        right = "█" * add_len + " " * (max_bar_width - add_len)

        print(f"{hour:02d}:00 |{left}│{right}| -{del_val} / +{add_val}")

    print("=" * 70)