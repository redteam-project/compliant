#!/usr/bin/env python

from github import Github
import pytz

timezone = pytz.timezone('America/New_York')

with open('access_token', 'r') as f:
    access_token = f.read()

github = Github(access_token)

rate = github.get_rate_limit()

remaining = rate.rate.remaining
limit = rate.rate.limit
reset_time = timezone.localize(rate.rate.reset)
print(str(remaining) + ' of ' + str(limit) + ' resets at ' + reset_time.isoformat())
