config_opts['chroot_setup_cmd'] += " ohpc-filesystem ohpc-buildroot"

config_opts['dnf.conf'] += """

[ohpc-release]
name=Open HPC - $basearch
baseurl=http://repos.openhpc.community/OpenHPC/2/CentOS_8/
failovermethod=priority
skip_if_unavailable=False

[ohpc-update]
name=Open HPC - $basearch update 2.4
baseurl=http://repos.openhpc.community/OpenHPC/2/update.2.4/CentOS_8/
failovermethod=priority
skip_if_unavailable=False
"""
