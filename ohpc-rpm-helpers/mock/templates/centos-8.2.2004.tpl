config_opts['chroot_setup_cmd'] = 'install tar gcc-c++ redhat-rpm-config redhat-release which xz sed make bzip2 gzip gcc coreutils unzip shadow-utils diffutils cpio bash gawk rpm-build info patch util-linux findutils grep'
config_opts['dist'] = 'el8'  # only useful for --resultdir variable subst
config_opts['releasever'] = '8'
config_opts['package_manager'] = 'dnf'
config_opts['extra_chroot_dirs'] = [ '/run/lock', ]
config_opts['bootstrap_image'] = 'quay.io/centos/centos:centos8.2.2004'


config_opts['dnf.conf'] = """
[main]
keepcache=1
debuglevel=2
reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
syslog_device=
metadata_expire=0
mdpolicy=group:primary
best=0
install_weak_deps=0
protected_packages=
module_platform_id=platform:el8
user_agent={{ user_agent }}

[baseos]
name=CentOS-$releasever - Base
baseurl=https://vault.centos.org/8.2.2004/BaseOS/$basearch/os/
failovermethod=priority
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official
gpgcheck=1
skip_if_unavailable=False

[appstream]
name=CentOS-$releasever - AppStream
baseurl=https://vault.centos.org/8.2.2004/AppStream/$basearch/os/
gpgcheck=1
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[powertools]
name=CentOS-$releasever - PowerTools
baseurl=https://vault.centos.org/8.2.2004/PowerTools/$basearch/os/
gpgcheck=1
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[devel]
name=CentOS-$releasever - Devel WARNING! FOR BUILDROOT USE ONLY!
baseurl=https://vault.centos.org/8.2.2004/Devel/$basearch/os/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[plus]
name=CentOS-$releasever - Plus
baseurl=https://vault.centos.org/8.2.2004/centosplus/$basearch/os/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[cr]
name=CentOS-$releasever - cr
baseurl=https://vault.centos.org/8.2.2004/cr/$basearch/os/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[debuginfo]
name=CentOS-$releasever - Debuginfo
baseurl=http://debuginfo.centos.org/8/$basearch/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[extras]
name=CentOS-$releasever - Extras
baseurl=https://vault.centos.org/8.2.2004/extras/$basearch/os/
gpgcheck=1
enabled=1
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[fasttrack]
name=CentOS-$releasever - fasttrack
baseurl=https://vault.centos.org/8.2.2004/fasttrack/$basearch/os/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[baseos-source]
name=CentOS-$releasever - BaseOS Sources
baseurl=https://vault.centos.org/8.2.2004/BaseOS/Source/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[appstream-source]
name=CentOS-$releasever - AppStream Sources
baseurl=https://vault.centos.org/8.2.2004/AppStream/Source/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[powertools-source]
name=CentOS-$releasever - PowerTools Sources
baseurl=https://vault.centos.org/8.2.2004/PowerTools/Source/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[extras-source]
name=CentOS-$releasever - Extras Sources
baseurl=https://vault.centos.org/8.2.2004/extras/Source/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official

[splus-source]
name=CentOS-$releasever - Plus Sources
baseurl=https://vault.centos.org/8.2.2004/centosplus/Source/
gpgcheck=1
enabled=0
gpgkey=file:///usr/share/distribution-gpg-keys/centos/RPM-GPG-KEY-CentOS-Official
"""
