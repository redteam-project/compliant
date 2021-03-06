redteam-project.compliant
=======================

This role applies security compliance baselines to Linux hosts.

Support is very good for RHEL and CentOS 7, pretty good for RHEL and CentOS 6, and Fedora is being worked.

The technical, automate-able controls in NIST 800-53 are our first goal, but don't worry, we'll be adding others later.

Note that this is not a "scanner" per-se.  If you wish to assess the application of this role to your host, check out the OpenSCAP project.

All tasks are tagged with the applicable controls.  To see which tasks are related to the "access control" category in the NIST 800-53 controls, execute the following.

Being updated
-------------

This role is currently being revamped. Refer to our issues or files in [files/gap](./files/gap) for more information.

Usage
-----

To generate a list of tasks that would be executed on a per-control-family basis:

```bash
$ ansible-playbook -i [inventory] --tags "NIST-800-53-AC" --list-tasks [playbook.yml]
```

Role Variables
--------------

```yaml
---
# vars file for compliant

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
# file: compliant.yaml
---
- hosts: compliant_hosts
  become: yes
  vars:
    scap_reports_dir: ~/scap_reports
  roles:
    - fedoraredteam.compliant
```

Example Inventory
-----------------

```ini
[compliant_hosts]
172.16.78.159
```

Example Run
-----------

```bash
ansible-playbook -u admin -i inventory compliant.yaml
```

License
-------

GPL v3


Provenance
------------------

This project is based on work by Ken Evensen, originally at https://github.com/rhtps/ansible-role-800-53, as well as OpenSCAP, which also borrowed heavily from Ken.
