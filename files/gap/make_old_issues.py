#!/usr/bin/env python

from github import Github
import json
from time import sleep

with open('issues.json', 'r') as f:
    old_issues = json.load(f)

with open('access_token', 'r') as f:
    access_token = f.read()

github = Github(access_token)
repo = github.get_repo('fedoraredteam/compliant')
milestone = repo.get_milestone(1)

for old_issue in old_issues:
    repo.create_issue(old_issue['title'], body=old_issue['body'], milestone=milestone)
    print(old_issue)
    sleep(15)
