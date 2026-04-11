def render_chart(hour_stats, max_bar_width=25):
    """
    把统计结果渲染成终端图表。
    """
    total_add = sum(v["add"] for v in hour_stats.values())
    total_del = sum(v["del"] for v in hour_stats.values())

    max_value = max(
        max(v["add"], v["del"]) for v in hour_stats.values()
    )
    if max_value == 0:
        max_value = 1

    print("=" * 70)
    print(f"代码增删时间段分布统计（总增加 +{total_add} 行，总删除 -{total_del} 行）")
    print("注：时间已自动转换为你当前机器所在的本地时区")
    print("图例：左侧为删除(-)，中间为0轴，右侧为增加(+)")
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