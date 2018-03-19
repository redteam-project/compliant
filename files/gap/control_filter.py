#!/usr/bin/env python

import os
import sys
import uuid
import yaml


def find_yaml(path):
    yaml_files = []
    for root, dirs, files in os.walk(path):
        for f in files:
            if '.yml' in f:
                yaml_files.append(root + '/' + f)
        for d in dirs:
            if d != '.':
                yaml_files.extend(find_yaml(d))
    return yaml_files


def process_tasks(tasks, filename):
    these_controls = []
    if isinstance(tasks, list):
        for task in tasks:
            task['uuid'] = str(uuid.uuid4())
            if task.get('tags'):
                for tag in task['tags']:
                    if 'NIST-800-53' in tag:
                        control = tag.replace('NIST-800-53-', '')
                        these_controls.append(control + ',' + task['name'] + ',' + filename + ',' + task['uuid'])
                    else:
                        these_controls.append(tag + ',' + task['name'] + ',' + filename + ',' + task['uuid'])
    if isinstance(tasks, dict):
        if tasks.get('tags'):
            task_uuid = str(uuid.uuid4())
            for tag in tasks['tags']:
                these_controls.append(tag + ',' + tasks['name'] + ',' + filename + ',' + task_uuid)
    return these_controls


try:
    plays = []
    for d in sys.argv[1:]:
        for yaml_file in find_yaml(d):
            with open(yaml_file, 'r') as f:
                play = yaml.load(f)
                for i, p in enumerate(play):
                    play[i]['filename'] = f.name
                plays.extend(play)
except Exception as e:
    print('ERROR: ' + str(e))
    exit(1)

all_controls = []
for play in plays:
    if play.get('tasks'):
        all_controls.extend(process_tasks(play['tasks'], play['filename']))
    elif play.get('name'):
        all_controls.extend(process_tasks(play, play['filename']))

print('control,name,file,uuid')
print('\n'.join(sorted(all_controls)))
