#!/usr/bin/env python

import yaml
import sys

try:
    with open(sys.argv[1], 'r') as f:
        content = yaml.load(f)
except Exception as e:
    print('ERROR: failed to read yaml file: ' + str(e))
    exit(1)

for play in content:
    for task in play['tasks']:
        if task.get('tags'):
            for tag in task['tags']:
                if 'NIST-800-53' in tag:
                    control = tag.replace('NIST-800-53-', '')
                    print(control + ',' + task['name'])
