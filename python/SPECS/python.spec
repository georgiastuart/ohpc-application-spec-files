#----------------------------------------------------------------------------bh-
# This RPM .spec file builds Mamba Package Manager to be compatible
# with the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#----------------------------------------------------------------------------eh-


%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 0
%define ohpc_python_dependent 0
%include %{_sourcedir}/OHPC_macros

# Base package name
%define pname python
%define vname 38

Name:       %{pname}%{vname}-%{compiler_family}%{PROJ_DELIM}
Version:    3.8.15
Release:    1%{?dist}
Summary:    Python
License:    Python License
URL:        https://www.python.org
Source0:    https://github.com/python/cpython/archive/refs/tags/v%{version}.tar.gz
Source1:    OHPC_setup_compiler

BuildRequires: zlib
BuildRequires: zlib-devel
BuildRequires: libffi-devel
BuildRequires: /usr/bin/pathfix.py
Requires: libffi

%define install_path %{OHPC_APPS}/%{compiler_family}/%{pname}%{vname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}

%description
The Python programming language and executables.

%prep
%setup -q -n c%{pname}-%{version}
pathfix.py -pni %{install_path}/bin/python3 .

%build
%ohpc_setup_compiler

./configure \
  --prefix=%{install_path} \
  --with-system-ffi
make

%install
make DESTDIR=%{buildroot} install 
ln -sr %{buildroot}%{install_path}/bin/python3 %{buildroot}%{install_path}/bin/python
ln -sr %{buildroot}%{install_path}/bin/pip3 %{buildroot}%{install_path}/bin/pip


# Module File
%{__mkdir_p}  %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}%{vname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}%{vname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}.lua
help([[
  This module loads the %{pname} programming language and executables.
  
  Version %{version}
]])

whatis("Name: Python")
whatis("Version: %{version}")
whatis("Description: %{summary}")
whatis("URL: %{url}")

local version = "%{version}"

prepend_path("PATH", "%{install_path}/bin")
prepend_path("INCLUDE", "%{install_path}/include")
prepend_path("LD_LIBRARY_PATH", "%{install_path}/lib")
prepend_path("MANPATH", "%{install_path}/man")

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}%{vname}/.version.%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}%{OHPC_CUSTOM_PKG_DELIM}"
EOF


%files
%dir %{OHPC_PUB}
%{install_path}
%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}%{vname}
%doc README.rst
%license LICENSE

%changelog
* Tue Dec 20 2022 Georgia Stuart <georgia.stuart@gmail.com> - 3.8.15
- Initial Python ohpc RPM

