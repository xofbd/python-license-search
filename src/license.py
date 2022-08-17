#!/usr/bin/env python3
"""
Determine frequency of licenses for Python projects
"""
from collections import Counter
from operator import itemgetter
import os
import re
import time

from dotenv import load_dotenv
import requests

from utils import cache

load_dotenv()
SLEEP_DURATON = 3
URL_BASE = "https://api.github.com"
HEADERS = {
    "User-Agent": os.getenv("GITHUB_USERNAME"),
    "Authorization": f"token {os.getenv('GITHUB_ACCESS_TOKEN')}",
}
CACHE_DIR = "cache"


@cache(CACHE_DIR)
def lookup_license(org, repo):
    """Return license of project given its GitHub org and repo"""
    url = f"{URL_BASE}/repos/{org}/{repo}"
    response = requests.get(url, headers=HEADERS)
    license_data = response.json()["license"]

    if license_data is not None:
        return license_data["name"]


def find_requirements(org, repo):
    """Return list of requirements of a project given its GitHub org and repo"""
    tree_data = get_tree_data(org, repo)
    requirement_files = parse_tree(tree_data)
    requirements = set()

    for file_name in requirement_files:
        requirements.update(parse_requirements(org, repo, file_name))

    return requirements


def get_tree_data(org, repo):
    """Return JSON of the data of the top-level tree given the org and repo"""
    url = f"{URL_BASE}/repos/{org}/{repo}/git/trees/HEAD"
    response = requests.get(url, headers=HEADERS)

    return response.json()


def parse_tree(tree_data):
    """Return paths that contain 3rd party dependencies from a project's tree"""
    if "tree" not in tree_data:
        return []

    return [
        path["path"] for path in tree_data["tree"]
        if re.search(r".*requirements.*\.txt", path["path"])
    ]


def parse_requirements(org, repo, file):
    """Return list of packages in the passed requirements file"""
    url = f"https://raw.githubusercontent.com/{org}/{repo}/HEAD/{file}"
    response = requests.get(url, headers=HEADERS)

    return re.findall(r"^([a-zA-Z0-9_-]+)", response.text, flags=re.MULTILINE)


def search_for_project(project):
    """Return GitHub URL from a project name, if any repos were found"""
    url = f"{URL_BASE}/search/repositories"
    params = {"q": f"{project}+language:python"}
    time.sleep(SLEEP_DURATON)
    response = requests.get(url, headers=HEADERS, params=params)
    search_result = response.json()

    if search_result["total_count"] != 0:
        return search_result["items"][0]["full_name"].split("/")


def print_results(license_count):
    """Print license results in descending order"""
    for license, count in sorted(license_count.items(), key=itemgetter(1), reverse=True):
        print(f"{license}: {count}")


def main():
    licenses = []
    seed_project = ("pandas-dev", "pandas")

    licenses.append(lookup_license(*seed_project))

    for requirement in find_requirements(*seed_project):
        project = search_for_project(requirement)
        if project is not None:
            licenses.append(lookup_license(*project))

    license_count = Counter(licenses)
    print_results(license_count)


if __name__ == "__main__":
    main()
