#!/usr/bin/env python

from github import Github
import jinja2
import csv
from time import sleep

with open('access_token', 'r') as f:
    access_token = f.read()

github = Github(access_token)
repo = github.get_repo('fedoraredteam/compliant')
milestone = repo.get_milestone(2)

all_controls = {}
template = jinja2.Environment(loader=jinja2.FileSystemLoader('./')).get_template('body.j2')
with open('controls_to_test.csv', 'r') as csvfile:
    controls = csv.reader(csvfile, delimiter=',', quotechar='"')
    for control in controls:
        control_name, title, filename, uuid_number, line_number = control
        if all_controls.get(uuid_number):
            all_controls[uuid_number]['tags'].append(control_name)
        else:
            all_controls[uuid_number] = {
                'tags': [control_name],
                'name': title,
                'filename': filename,
                'line_number': line_number,
                'uuid_number': uuid_number
            }

count = 0
count_keys = len(all_controls.keys())
for uuid in all_controls.keys():
    all_controls[uuid]['body'] = template.render(all_controls[uuid])
    extant_issues = github.search_issues(query=all_controls[uuid]['name'])
    1
    repo.create_issue(all_controls[uuid]['name'], body=all_controls[uuid]['body'], milestone=milestone)
    print(str(count) + '/' + str(count_keys) + ' created "' + all_controls[uuid]['name'] + '"')
    count += 1
    sleep(15)

