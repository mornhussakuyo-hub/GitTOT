import subprocess

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
        raise RuntimeError("Failed to run git log. Please make sure the current directory is a Git repository.")

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
                    "del": current_del,
                })

            parts = line.split("|")
            current_timestamp = int(parts[2])
            current_add = 0
            current_del = 0

        else:
            parts = line.split("\t")
            if len(parts) == 3:
                added, deleted, _filename = parts
                if added != "-":
                    current_add += int(added)
                if deleted != "-":
                    current_del += int(deleted)

    if current_timestamp is not None:
        commits.append({
            "timestamp": current_timestamp,
            "add": current_add,
            "del": current_del,
        })

    return commits


def get_local_commits():
    output = run_git_log()
    return parse_git_log(output)