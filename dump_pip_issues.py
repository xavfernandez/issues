import json
import os

from github3 import login

GITHUB_TOKEN_PATH = os.path.expanduser('~/.config/github_token')
GITHUB_USERNAME = 'xavfernandez'
OUTPUT_DIR = 'build'

with open(GITHUB_TOKEN_PATH, 'r') as fd:
    token = fd.readline().strip()
gh = login(GITHUB_USERNAME, token=token)

pip_issues = list(gh.iter_repo_issues('pypa', 'pip', state='all'))

pip_issues_data = [issue._json_data for issue in pip_issues]
with open(os.path.join(OUTPUT_DIR, 'pip_issues.data'), 'w') as f:
    json.dump(pip_issues_data, f)
