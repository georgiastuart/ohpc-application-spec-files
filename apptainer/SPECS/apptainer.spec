#----------------------------------------------------------------------------bh-
# This RPM .spec file builds Apptainer to be compatible
# with the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
# Heavily inspired by
# https://src.fedoraproject.org/rpms/conda/blob/rawhide/f/conda.spec
#----------------------------------------------------------------------------eh-

%include %{_sourcedir}/OHPC_macros

# Base package name
%define pname apptainer

%define singgopath src/github.com/apptainer/%{pname}-%{version}

Summary: Application and environment virtualization
Name: %{pname}%{PROJ_DELIM}
Version: 1.1.0
Release: 1
# https://spdx.org/licenses/BSD-3-Clause-LBNL.html
License: BSD-3-Clause-LBNL
Group: %{PROJ_NAME}/runtimes
URL: https://apptainer.org/
Source0: https://github.com/apptainer/apptainer/releases/download/v%{version}/apptainer-%{version}.tar.gz
Patch1: singularity-suse-timezone.patch
ExclusiveOS: linux
BuildRequires: gcc
BuildRequires: git
BuildRequires: openssl-devel
BuildRequires: libuuid-devel
BuildRequires: libseccomp-devel
Requires: file
%if 0%{?suse_version}
BuildRequires: go1.14
BuildRequires: binutils-gold
Requires: squashfs
%else
BuildRequires: golang > 1.6
Requires: squashfs-tools
%endif
BuildRequires: cryptsetup
#!BuildIgnore: post-build-checks rpmlint-Factory

# Default library install path
%define install_path %{OHPC_LIBS}/%{pname}/%version

%description
Apptainer provides functionality to make portable
containers that can be used across host environments.

%prep
# Create our build root
rm -rf %{name}-%{version}
mkdir %{name}-%{version}

%build
cd %{name}-%{version}

mkdir -p gopath/%{singgopath}
tar -C "gopath/src/github.com/apptainer/" -xf "%SOURCE0"

export GOPATH=$PWD/gopath
export PATH=$GOPATH/bin:$PATH
cd $GOPATH/%{singgopath}

./mconfig -V %{version} \
    --prefix=%{install_path} \
    --without-suid

cd builddir
make old_config=

%install
cd %{name}-%{version}

export GOPATH=$PWD/gopath
export PATH=$GOPATH/bin:$PATH
cd $GOPATH/%{singgopath}/builddir

mkdir -p $RPM_BUILD_ROOT%{install_path}/share/man/man1
make DESTDIR=$RPM_BUILD_ROOT install

# NO_BRP_CHECK_RPATH has no effect on CentOS 7
export NO_BRP_CHECK_RPATH=true


# OpenHPC module file
%{__mkdir_p} %{buildroot}%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}.lua
help (
[[

This module loads the %{pname} utility

Version %{version}

]])

whatis ("Name: %{pname}")
whatis ("Version: %{version}")
whatis ("Category: runtime")
whatis ("Description: %{summary}")
whatis ("URL: %{url}")

prepend_path("PATH","%{install_path}/bin")
prepend_path("MANPATH","%{install_path}/share/man")

setenv ("%{PNAME}_DIR","%{install_path}")
setenv ("%{PNAME}_BIN","%{install_path}/bin")

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/.version.%{version}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}"
EOF

%{__mkdir_p} ${RPM_BUILD_ROOT}/%{_docdir}

%files
%dir %{install_path}/etc/apptainer
%config(noreplace) %{install_path}/etc/apptainer/*
%{OHPC_PUB}
