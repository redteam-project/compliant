#!/usr/bin/python
# -*- coding: utf-8 -*-
# (c) 2017, Kenneth D. Evensen <kdevensen@gmail.com>

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


ANSIBLE_METADATA = {'metadata_version': '1.1',
                    'status': ['preview'],
                    'supported_by': 'community'}


DOCUMENTATION = """
module: aide_ruleset
author:
    - "Kenneth D. Evensen (@kevensen)"
short_description: Manage AIDE Rule Sets
description:
  - Edit an AIDE ruleset in specified AIDE configuration file. See
    man(5) aide.conf for details.
version_added: "2.6"
options:

"""

EXAMPLES = """

"""

RETURN = '''

...
'''

from ansible.module_utils.basic import AnsibleModule
import re
from tempfile import NamedTemporaryFile

PATTERN = r"(?P<name>^[A-Z_]+)\s?=\s?(?P<options>.*)$"
RULESET_REGEX = re.compile(PATTERN, re.MULTILINE)

def add_options(existing_options, options_to_add):
    changed = False
    options_added = []

    # Create a list of new args that aren't already present
    options_added = [option for option in options_to_add if option not in existing_options]
    
    if options_added:
        existing_options = existing_options + options_added
        changed = True

    return changed, existing_options, options_added

def remove_options(existing_options, options_to_remove):
    changed = False
    options_removed = []

    # Let's check to see if there are any args to remove by finding the intersection
    # of the rule's current args and the args_to_remove lists
    if list(set(existing_options) & set(options_to_remove)):
        # There are args to remove, so we create a list of new_args absent the args
        # to remove.
        existing_options = [option for option in existing_options if option not in options_to_remove]
        options_removed = [option for option in existing_options if option in options_to_remove]
        changed = True


    return changed, existing_options, options_removed

def ruleset_pattern(name):
    return r"^" + name + r"\s?=\s?.*$"

def update_content(content, rulesets):
    # Update the content
    for ruleset, options in rulesets.iteritems():
        replacement = ruleset + " = " + "+".join(options)
        content = re.sub(ruleset_pattern(ruleset), replacement, content)

    return content

def main():

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, type='str'),
            conf_path=dict(required=False, default='/etc/aide.conf', type='path'),
            options=dict(required=False, type='list'),
            options_string=dict(required=False, type='str'),
            state=dict(required=False, default="updated",
                       choices=['absent', 'present', 'updated']),
            backup=dict(default=False, type='bool'),
            add_if_not_present=dict(default=False, required=False)
        ),
        supports_check_mode=True,
        mutually_exclusive=[
            ['options', 'options_string']
        ],
        required_one_of=[
            ['options', 'options_string']
        ]
    )
    # For existing rule sets
    rulesets = dict()
    content = str()
    options = []
    options_changed = []
    existing_options = []
    backupdest = ""
    fname = module.params['conf_path']
    action = module.params['state']
    add_if_not_present = module.params['add_if_not_present']
    ruleset_name = module.params['name'].rstrip().lstrip()

    # Get the options from either the 'options' or 'options_string' module arguments
    if module.params['options']:
        options = module.params['options']
    else:
        options = module.params['options_string'].split('+')

    # Open the file and read the content or fail
    try:
        with open(fname, 'r') as aide_file_obj:
            content = aide_file_obj.read()
    except IOError as e:
        # If unable to read the file, fail out
        module.fail_json(msg='Unable to open/read AIDE configuration \
                            file %s with error %s.' %
                         (fname, str(e)))
    matches = RULESET_REGEX.findall(content)
    # Load existing rule set
    for match in matches:
        existing_options = match[1].split('+')
        rulesets[match[0]] = existing_options

    module.log(msg="EXISTING RULESET KEYS: " + str(rulesets.keys()))
    module.log(msg="EXISTING RULESET: " + str(rulesets))

    # Take action
    if action == 'absent':
        changed, rulesets[ruleset_name], options_changed = remove_options(rulesets[ruleset_name], options)
    elif action == 'present':
        changed, rulesets[ruleset_name], options_changed = add_options(rulesets[ruleset_name], options)
    elif action == 'updated':
        if ruleset_name in rulesets.keys() or add_if_not_present:
            rulesets[ruleset_name] = options
            options_changed = options
            changed = True


    # Write file
    if not module.check_mode and changed:
        module.log(msg="WRITING")
        # Update the content
        pattern = r"^" + ruleset_name + r"\s?=\s?.*$"
        module.log(msg="PATTERN: " + pattern)
        replacement = ruleset_name + " = " + "+".join(rulesets[ruleset_name])
        module.log(msg="REPLACEMENT: " + replacement)
        new_content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        
        module.log(msg="OLD CONTENT equals NEW CONTENT: " + str(content == new_content))
        # First, create a backup if desired.
        if module.params['backup']:
            backupdest = module.backup_local(fname)
        # Write the file
        try:
            temp_file = NamedTemporaryFile(mode='w')
            module.log(msg="TEMP FILE NAME: " + temp_file.name)
            with open(temp_file.name, 'w') as fd:
                fd.write(new_content)

        except IOError:
            module.fail_json(msg='Unable to create temporary \
                                    file %s' % temp_file)

        module.atomic_move(temp_file.name, fname)


    facts = {}
    facts['aide_ruleset'] = {'action': action,
                             'name': ruleset_name,
                             'existing_options': existing_options,
                             'options_changed': options_changed,
                             'backupdest': backupdest}

    module.exit_json(changed=changed, ansible_facts=facts)

if __name__ == '__main__':
    main()