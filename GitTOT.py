import subprocess
from collections import defaultdict
from datetime import datetime
import sys


def run_git_log():
    cmd = [
        "git",
        "log",
        "--numstat",
        "--pretty=format:COMMIT|%H|%ct"
    ]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )

    if result.returncode != 0:
        print("运行 git log 失败，请确认当前目录是一个 git 仓库。")
        print(result.stderr)
        sys.exit(1)

    return result.stdout


def parse_git_log(output: str):

    commits = []

    current_timestamp = None
    current_add = 0
    current_del = 0

    lines = output.splitlines()

    for line in lines:
        if line.startswith("COMMIT|"):
            if current_timestamp is not None:
                commits.append({
                    "timestamp": current_timestamp,
                    "add": current_add,
                    "del": current_del
                })

            parts = line.split("|")
            if len(parts) != 3:
                continue

            current_timestamp = int(parts[2])
            current_add = 0
            current_del = 0

        else:
            parts = line.split("\t")
            if len(parts) < 3:
                continue

            add_str, del_str, _filename = parts[0], parts[1], parts[2]

            if add_str == "-" or del_str == "-":
                continue

            try:
                current_add += int(add_str)
                current_del += int(del_str)
            except ValueError:
                continue

    if current_timestamp is not None:
        commits.append({
            "timestamp": current_timestamp,
            "add": current_add,
            "del": current_del
        })

    return commits

def group_by_hour(commmits):

    hour_stats={h:{"add":0,"del":0}for h in range(24)}

    for commit in commits:
        dt=datetime.fromtimestap(commit["timestamp"])
        hour=dt.hour
        hour_stats[hour]["add"] += commit["add"]
        hour_stats[hour]["del"] += commit["del"]
    
    return hour_stats

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
    print(f"📊 代码增删时间段分布统计（总增加 +{total_add} 行，总删除 -{total_del} 行）")
    print("注：时间已自动转换为你当前机器所在的本地时区")
    print("图例：左侧为删除(-)，中间为0轴，右侧为增加(+)")
    print()

    for hour in range(24):
        add_val = hour_stats[hour]["add"]
        del_val = hour_stats[hour]["del"]

        add_len = int(add_val / max_value * max_bar_width)
        del_len = int(del_val / max_value * max_bar_width)

        left = " " * (max_bar_width - del_len) + "█" * del_len
        right = "█" * add_len + " " * (max_bar_width - add_len)

        print(f"{hour:02d}:00 |{left}│{right}| -{del_val} / +{add_val}")

    print("=" * 70)


def main():
    output = run_git_log()
    commits = parse_git_log(output)
    hour_stats = group_by_hour(commits)
    render_chart(hour_stats)


if __name__ == "__main__":
    main()