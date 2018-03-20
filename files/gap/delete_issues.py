#!/usr/bin/env python

from github import Github
import pydevd
from time import sleep

with open('access_token', 'r') as f:
    access_token = f.read()

github = Github(access_token)
repo = github.get_repo('fedoraredteam/compliant')

issues = repo.get_issues(state='open')
for issue in issues:
    # pydevd.settrace()
    issue.edit(state='closed')
    print('closed issue ' + str(issue.number))
    sleep(5)
