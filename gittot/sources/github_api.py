from urllib.parse import urlparse
from datetime import datetime
import requests

def parse_github_repo_url(repo_url: str):
    parsed=urlparse(repo_url)

    if parsed.netloc not in ("github.com","www.github.com") :
        raise ValueError("Not a github.com repo.")
    
    path = parsed.path.strip("/")
    if path.endswith(".git"):
        path=path[:-4]

    parts=[part for part in path.split("/") if part]
    if len(parts)<2:
        raise ValueError("The repository link format is incorrect and should be similar to https://github.com/owner/repo")
    
    owner = parts[0]
    repo = parts[1]
    return owner,repo

def build_headers(token=None):
    headers = {
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    if token:
        headers["Authorization"] = f"token {token.strip()}"

    return headers


def list_commit_shas(owner, repo, token=None, max_commits=None):
    headers = build_headers(token)
    page = 1
    per_page = 100
    result = []
    while True:
        url = f"https://api.github.com/repos/{owner}/{repo}/commits"
        resp = requests.get(
            url,
            headers=headers,
            params={"per_page": per_page, "page": page},
            timeout=30,
        )
        if resp.status_code == 401:
            raise RuntimeError(f"GitHub authentication failed: {resp.text}")
        if resp.status_code == 404:
            raise RuntimeError("The repository does not exist, or you do not have access rights.")
        if resp.status_code == 403:
            raise RuntimeError(f"GitHub API request was denied: {resp.text}")
        if resp.status_code != 200:
            raise RuntimeError(f"Failed to get commit list: {resp.status_code} {resp.text}")

        data = resp.json()
        if not data:
            break

        for item in data:
            result.append(item["sha"])
            if max_commits is not None and len(result) >= max_commits:
                return result

        if len(data) < per_page:
            break

        page += 1

    return result

def fetch_commit_detail(owner, repo, sha, token=None):
    headers = build_headers(token)
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"

    resp = requests.get(url, headers=headers, timeout=30)

    if resp.status_code == 401:
        raise RuntimeError(f"GitHub authentication failed: {resp.text}")
    if resp.status_code == 404:
        raise RuntimeError(f"commit does not exist or access is denied: {sha}")
    if resp.status_code == 403:
        raise RuntimeError(f"GitHub API request was denied: {resp.text}")
    if resp.status_code != 200:
        raise RuntimeError(f"Failed to get commit details: {resp.status_code} {resp.text}")

    data = resp.json()

    commit_time_str = data["commit"]["author"]["date"]
    timestamp = int(datetime.fromisoformat(commit_time_str.replace("Z", "+00:00")).timestamp())

    stats = data.get("stats", {})
    additions = stats.get("additions", 0)
    deletions = stats.get("deletions", 0)

    return {
        "timestamp": timestamp,
        "add": additions,
        "del": deletions,
    }


def get_github_commits(repo_url, token=None, max_commits=None):
    owner, repo = parse_github_repo_url(repo_url)

    shas = list_commit_shas(
        owner=owner,
        repo=repo,
        token=token,
        max_commits=max_commits,
    )

    commits = []
    for sha in shas:
        commits.append(
            fetch_commit_detail(
                owner=owner,
                repo=repo,
                sha=sha,
                token=token,
            )
        )

    return commits
