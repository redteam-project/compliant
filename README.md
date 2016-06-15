800-53
=========

This role endeavors to apply relavent NIST 800-53 controls to an Enterprise Linux host.

This is not a "scanner" per-se.  If you wish to assess the application of this role to your host, check out the Scap Security Guide and Open SCAP projects.  Both of these will provide you tools with which you can scan your host.

Requirements
------------

You must have the appropriate disk partitions create on your host: /var, /var/log, /var/log/audit

<strong>NOTE:</strong> This will make sweeping changes to your host.  It is recommended you apply this role to a freshly provisioned host.

Role Variables
--------------
```yaml
---
# vars file for 800-53

#The location where to place the audit rules file on the host
audit_rules: /etc/audit/rules.d/audit.rules

#The architecture(s) to for which the audit rules should apply
audit_arch:
  - b32
  - b64

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

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

    - hosts: servers
      roles:
         - { role: username.rolename, x: 42 }

License
-------

Apache 2.0

Author Information
------------------

Ken Evensen is a Solutions Architect with Red Hat
