#!/usr/bin/env python3

"""
open_prs.py lists all the open pull requests for the repositories provided in
`repos` for the users specified in `usernames`.
You have to have your Github API token in then environment variable
`GITHUB_TOKEN_GALAXY`.
"""

__author__ = "Jochen Breuer"
__email__  = "jbreuer@suse.de"
__license__ = "GPLv3"

import os
import sys
import toml
import requests
from os.path import expanduser
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from dateutil import parser


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_prs_for_user(username, api_token):
    """\
    Fetches the pull requests for the given user and returns
    the data set as a dict.
    """
    query = """
    {
    user(login: "%s") {
        name
        login
        pullRequests(first: 100, states: OPEN) {
        totalCount
        nodes {
            repository {
            id
            nameWithOwner
            }
            createdAt
            number
            title
            url
        }
        pageInfo {
            hasNextPage
            endCursor
        }
        }
    }
    }
    """ % username
    url = 'https://api.github.com/graphql'
    json = { 'query' : query }
    headers = {'Authorization': 'token %s' % api_token}

    r = requests.post(url=url, json=json, headers=headers)
    return r.json()


def get_colour_coding_for_pr(pr, days=14):
    """\
    Returns the colour code needed to print to the CLI.
    The colour is green, unless the pr is > `days` old.
    """
    created_at = parser.parse(pr['createdAt'])
    now = datetime.now(timezone.utc)
    age = now - created_at
    colour = bcolors.OKGREEN
    if age > timedelta(days=days):
        colour = bcolors.FAIL
    return colour


def get_settings():
    """\
    Loads TOML settings from the provided file and returns a usernames and
    repos.
    """
    paths = (
        "./.open_prs.toml",
        "./open_prs.toml",
        "~/.open_prs.toml",
        "~/.config/open_prs.toml",
        "/etc/open_prs.toml",
    )
    settings = None
    for path in paths:
        path = expanduser(path)
        if os.path.isfile(path) and not os.path.isdir(path) and not os.path.islink(path):
            settings = toml.load(path)
    if not settings:
        print("Could not find settings file in any of these locations: {}".format(", ".join(paths)))
        sys.exit(3)
    if "usernames" not in settings:
        print("usernames definition missing in settings file: repos = [\"bob\", \"alice\"]", file=sys.stderr)
        sys.exit(2)
    if "repos" not in settings:
        print("repos definition missing in settings file: repos = [\"foo/prj\", \"bar/prj\"]", file=sys.stderr)
        sys.exit(2)
    usernames = settings['usernames']
    repos = settings['repos']
    github_token = None
    if "github_token" in settings:
        github_token = settings['github_token']
    return usernames, repos, github_token


def filter_prs_by_repos(pull_requests, repos):
    """\
    Returns only the pull requests that are listed in repos.
    """
    return [pull_request for pull_request in pull_requests if pull_request['repository']['nameWithOwner'] in repos]


if __name__ == "__main__":
    api_token = None
    usernames, repos, api_token = get_settings()
    if not api_token:
        api_token = os.environ.get('GITHUB_TOKEN_GALAXY')
    if not api_token:
        print("Please provide a Github API token via environment variable `GITHUB_TOKEN_GALAXY` or via settings file.", file=sys.stderr)
        sys.exit(1)
    for username in usernames:
        data = get_prs_for_user(username, api_token)
        print("{}{}{}".format(bcolors.OKBLUE, data['data']['user']['name'], bcolors.ENDC))
        print("=" * 80)
        pull_requests = filter_prs_by_repos(data['data']['user']['pullRequests']['nodes'], repos)
        if len(pull_requests) == 0:
            print("No pull requests!")
        for i, pr in enumerate(pull_requests):
            title = pr['title']
            repo = pr['repository']['nameWithOwner']
            if repo not in repos:
                continue
            url = pr['url']
            print("{}{}{}".format(get_colour_coding_for_pr(pr), title, bcolors.ENDC))
            print("🔗 {}".format(url))
            if i+1 == len(pull_requests):
                print("\n")
                continue
            print("-" * 80)
