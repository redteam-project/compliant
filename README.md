fedoraredteam.compliant
=======================

This role applies security compliance baselines to Linux hosts.

The technical, automate-able controls in NIST SP800-53 are our first goal, but don't worry, we'll be adding others later.

This is not a "scanner" per-se.  If you wish to assess the application of this role to your host, check out the OpenSCAP project.

All tasks are tagged with the applicable controls.  To see which tasks are related to the "access control" category in the NIST 800-53 controls, execute the following.

Being updated
-------------

This role is currently being revamped. Refer to our issues or files in [files/gap](./files/gap) for more information.

**New Layout**

A goal of this revamp is to make this role more cross-platform and cross-standard. So this is the layout to expect in the role directories:

```
├── main.yml                    # main role file
├── access_control
│   ├── centos.yml
│   ├── fedora.yml
│   ├── main.yml                # Linux generic AC controls
│   └── rhel.yml                # RHEL-specific AC controls
├── audit_and_accountability
│   ├── centos.yml
│   ├── fedora.yml
│   ├── main.yml                # Linux generic AU controls
│   └── rhel.yml                # RHEL-specific AU controls
...
```

Another goal of this project is cross-standard support. However, the NIST control famlies are prety well-generalized, so we're standardizing those for now.

To generate a list of tasks that would be executed on a per-control-family basis:

```bash
$ ansible-playbook -i [inventory] --tags "AC" --list-tasks [playbook.yml]
```

Role Variables
--------------

```yaml
---
# vars file for 800-53

#The schedule for AIDE
aide_minute: 05
aide_hour: 03
aide_day_of_month: '*'
aide_month: '*'
aide_day_of_week: '*'

vpn_package: openswan
#Whether or not to run an SCAP scan
run_scap: true
#The profile to run
scap_profile:
  - stig-rhel{{ ansible_distribution_major_version }}-server-upstream
#Where on your local host you wish to place the reports
scap_reports_dir: /tmp
```

Dependencies
------------

ansible 2.2.0.0

Example Playbook
----------------

```yaml
# file: 80053.yaml
---
- hosts: 80053_hosts
  become: yes
  vars:
    scap_reports_dir: ~/scap_reports
  roles:
    - ansible-role-800-53
```

Example Inventory
-----------------

```ini
[80053_hosts]
172.16.78.159
```

Example Run
-----------

```bash
ansible-playbook -u admin -i 80053_inventory 80053.yaml
```

License
-------

GPL v3


Provenance
------------------

This project is based on work by Ken Evensen, originally at https://github.com/rhtps/ansible-role-800-53.

When we borrow things from other open source projects we try to indicate when we've done so via inline comments. 

