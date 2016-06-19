800-53
=========

This role endeavors to apply relevant NIST 800-53 controls to an Enterprise Linux host.

This is not a "scanner" per-se.  If you wish to assess the application of this role to your host, check out the SCAP Security Guide and Open SCAP projects.  Both of these will provide you tools with which you can scan your host.

The tasks are organized by 800-53 category.  Yes, some tasks are repeated in multiple categories.

Requirements
------------

Per 800-53 Audit and Accountability requirements, you are recommended to have the following partitions:
1. /var
2. /var/log
3. /var/log/audit
4. /home
5. /tmp

These scripts will not create these partitions for you.

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

#The services to disable via the access control set of tasks
ac_disable_services:
- autofs
- abrtd
- rdisc
- rexec
- rlogin
- rsh
- telnet
- tftp
- xinetd
- ypbind
- ypserv

#The packages to uninstall via the access control set of tasks
ac_uninstall_packages:
- xinetd
- telnet-server
- rsh-server
- ypserv
- tftp-server

#The services to disable via the configuration management set of tasks
cm_disable_services:
- atd
- avahi-daemon
- oddjobd
- qpidd
- rdisc
- rexec
- rlogin
- rsh
- telnet
- tftp
- xinetd
- ypbind

#The packages to uninstall via the configuration management set of tasks
cm_uninstall_packages:
- xinetd
- telnet-server
- rsh-server
- ypserv
- tftp-server

#The services to disable via the identification and authentication set of tasks
ia_disable_services:
- telnet
- rlogin
- rsh

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

None

Example Playbook
----------------

```yaml
# file: scap.yaml
- hosts: scap_hosts
  roles:
  - ansible-role-800-53
  vars:
    scap_reports_dir: ~/scap_reports
```
Example Inventory
-----------------
```ini
[scap_hosts]
172.16.78.159
```
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
