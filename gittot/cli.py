import argparse
import os
import sys

from gittot.config import bind_token,get_bound_token,unbind_token
from gittot.render import render_output
from gittot.stats import GROUP_BY_CHOICES, group_commits
from gittot.sources.local_git import get_local_commits
from gittot.sources.github_api import get_github_commits
from gittot.time_filters import normalize_time_filters

def build_parser():
    parser=argparse.ArgumentParser(
        prog="gittot",
        description="Analyze git code additions and deletions across multiple time buckets."
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
    parser.add_argument(
        "--since",
        help="Only include commits on or after this date/time"
    )
    parser.add_argument(
        "--until",
        help="Only include commits on or before this date/time"
    )
    parser.add_argument(
        "--author",
        help="Only include commits by an author name or email"
    )
    parser.add_argument(
        "--branch",
        help="Only include commits reachable from this branch"
    )
    parser.add_argument(
        "--by",
        choices=GROUP_BY_CHOICES,
        default="hour",
        help="Group results by hour, weekday, date, or month"
    )
    parser.add_argument(
        "--format",
        choices=("chart", "json", "csv"),
        default="chart",
        help="Render output as a terminal chart, JSON, or CSV"
    )

    parser.add_argument(
        "--bind",
        help="Bind and save GitHub token locally, then exit"
    )
    parser.add_argument(
        "--unbind",
        action="store_true",
        help="Remove the locally saved GitHub token, then exit"
    )
    parser.add_argument(
        "--show-bind",
        action="store_true",
        help="Show whether a local GitHub token is currently bound"
    )

    return parser

def main():
    parser=build_parser()
    args=parser.parse_args()

    try:
        if args.bind:
            bind_token(args.bind)
            print("GitHub token has been saved locally.")
            return
        if args.unbind:
            removed = unbind_token()
            if removed:
                print("Local GitHub token has been removed.")
            else:
                print("No local GitHub token was bound.")
            return
        if args.show_bind:
            token = get_bound_token()
            if token:
                print("A local GitHub token is currently bound.")
            else:
                print("No local GitHub token is currently bound.")
            return
        
        effective_token = args.token or get_bound_token() or os.environ.get("GITHUB_TOKEN")
        since, until = normalize_time_filters(args.since, args.until)

        if args.repo:
            commits=get_github_commits(
                repo_url=args.repo,
                token=effective_token,
                max_commits=args.max_commits,
                since=since,
                until=until,
                author=args.author,
                branch=args.branch,
            )
        else:
            commits=get_local_commits(
                since=since,
                until=until,
                author=args.author,
                branch=args.branch,
            )
        
        if not commits:
            print("No commit data was retrieved.")
            sys.exit(1)
        
        grouped_commits=group_commits(commits, group_by=args.by)
        render_output(grouped_commits, group_by=args.by, output_format=args.format)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    
