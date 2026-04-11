import argparse
import sys

from gittot.stats import group_by_hour
from gittot.render import render_chart
from gittot.sources.local_git import get_local_commits
from gittot.sources.github_api import get_github_commits

def build_parser():
    parser=argparse.ArgumentParser(
        prog="gittot",
        description="Analyze git code additions and deletions by hour."
    )

    parser.add_argument(
        "--repo",
        help="GitHub repository URL, e.g. https://github.com/owner/repo"
    )

    parser.add_argument(
        "--token",
        help="GitHub token for authenticated API requests"
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=None,
        help="Maximum number of commits to fetch from remote repository"
    )

    return parser

def main():
    parser=build_parser()
    args=parser.parse_args()

    try:
        if args.repo:
            commits=get_github_commits(
                repo_url=args.repo,
                token=args.token,
                max_commits=args.max_commits,
            )
        else:
            commits=get_local_commits()
        
        if not commits:
            print("No commit data was retrieved.")
            sys.exit(1)
        
        hour_stats=group_by_hour(commits)
        render_chart(hour_stats)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    