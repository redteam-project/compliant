#!/usr/bin/env python

from github import Github
import json

with open('issues.json', 'r') as f:
    old_issues = json.load(f)

with open('access_token', 'r') as f:
    access_token = f.read()

github = Github(access_token)
repo = github.get_repo('fedoraredteam/compliant')

for old_issue in old_issues:
    repo.create_issue(old_issue['title'], body=old_issue['body'])



