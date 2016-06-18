800-53
=========

This role endeavors to apply relevant NIST 800-53 controls to an Enterprise Linux host.

This is not a "scanner" per-se.  If you wish to assess the application of this role to your host, check out the SCAP Security Guide and Open SCAP projects.  Both of these will provide you tools with which you can scan your host.

Requirements
------------

You must have the appropriate disk partitions create on your host: /var, /var/log, /var/log/audit

<strong>NOTE:</strong> This will make sweeping changes to your host.  It is recommended you apply this role to a freshly provisioned host.

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

#The location(s) of the shared libraries on the target host
shared_lib_path:
  - /lib
  - /lib64
  - /usr/lib
  - /usr/lib64

#The location of the executable(s) on the target host
executables_path:
  - /bin
  - /usr/bin
  - /usr/local/bin
  - /sbin
  - /usr/sbin
  - /usr/local/sbin
```
Dependencies
------------

None

Example Playbook
----------------

	---
	# file: scap.yaml
	- hosts: scap_hosts
	  roles:
	  - ansible-role-800-53
	  vars:
    	scap_reports_dir: ~/scap_reports

Example Run
-----------
```bash
ansible-playbook -u admin -b -i scap_inventory scap.yaml
```

License
-------

Apache 2.0

Author Information
------------------

Ken Evensen is a Solutions Architect with Red Hat
