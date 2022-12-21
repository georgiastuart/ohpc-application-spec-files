#----------------------------------------------------------------------------bh-
# This RPM .spec file builds Python to be compatible
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
%define python3_version 3.8

# Setuptools and dependencies
%define setuptools_version 65.6.3
%define setuptools_scm_version 7.1.0
%define packaging_version 22.0
%define flit_version 3.8.0
%define tomli_version 2.0.1
%define typing_extensions_version 4.4.0
%define wheel_version 0.38.4

Name:       %{pname}%{vname}-%{compiler_family}%{PROJ_DELIM}
Version:    3.8.15
Release:    1%{?dist}
Summary:    Python
License:    Python License
URL:        https://www.python.org
Source0:    https://github.com/python/cpython/archive/refs/tags/v%{version}.tar.gz#/c%{pname}-%{version}.tar.gz
Source1:    https://files.pythonhosted.org/packages/b6/21/cb9a8d0b2c8597c83fce8e9c02884bce3d4951e41e807fc35791c6b23d9a/setuptools-%{setuptools_version}.tar.gz
Source2:    https://files.pythonhosted.org/packages/98/12/2c1e579bb968759fc512391473340d0661b1a8c96a59fb7c65b02eec1321/setuptools_scm-%{setuptools_scm_version}.tar.gz
Source3:    https://files.pythonhosted.org/packages/6b/f7/c240d7654ddd2d2f3f328d8468d4f1f876865f6b9038b146bec0a6737c65/packaging-%{packaging_version}.tar.gz
Source4:    https://files.pythonhosted.org/packages/28/c6/c399f38dab6d3a2518a50d334d038083483a787f663743d713f1d245bde3/flit-%{flit_version}.tar.gz
Source5:    https://files.pythonhosted.org/packages/10/e5/be08751d07b30889af130cec20955c987a74380a10058e6e8856e4010afc/flit_core-%{flit_version}.tar.gz
Source6:    https://files.pythonhosted.org/packages/c0/3f/d7af728f075fb08564c5949a9c95e44352e23dee646869fa104a3b2060a3/tomli-%{tomli_version}.tar.gz
Source7:    https://files.pythonhosted.org/packages/e3/a7/8f4e456ef0adac43f452efc2d0e4b242ab831297f1bac60ac815d37eb9cf/typing_extensions-%{typing_extensions_version}.tar.gz
Source8:    https://files.pythonhosted.org/packages/a2/b8/6a06ff0f13a00fc3c3e7d222a995526cbca26c1ad107691b6b1badbbabf1/wheel-%{wheel_version}.tar.gz
Source9:    OHPC_setup_compiler

BuildRequires: zlib
BuildRequires: zlib-devel
BuildRequires: libffi-devel
BuildRequires: openssl-devel
BuildRequires: /usr/bin/pathfix.py
Requires: libffi
Requires: openssl
Requires: zlib

%define install_path %{OHPC_APPS}/%{compiler_family}/%{pname}%{vname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}

%description
The Python programming language and executables.

%prep
%setup -q -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -n c%{pname}-%{version}

%build
%ohpc_setup_compiler

./configure \
  --prefix=%{install_path} \
  --with-system-ffi
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install
ln -sr %{buildroot}%{install_path}/bin/python3 %{buildroot}%{install_path}/bin/python
ln -sr %{buildroot}%{install_path}/bin/pip3 %{buildroot}%{install_path}/bin/pip

# Install some nice utilities like setuptools
export PYTHONPATH="%{buildroot}%{install_path}/lib64/python%{python3_version}/site-packages:%{buildroot}%{install_path}/lib/python%{python3_version}/site-packages:$PYTHONPATH"
export PATH="%{buildroot}%{install_path}/bin:$PATH"

python3.8 -m pip install --no-index --no-build-isolation --prefix=%{buildroot}%{install_path} wheel-%{wheel_version}/
python3.8 -m pip install --no-index --no-build-isolation --prefix=%{buildroot}%{install_path} setuptools-%{setuptools_version}/
python3.8 -m pip install --no-index --no-build-isolation --prefix=%{buildroot}%{install_path} flit_core-%{flit_version}/
python3.8 -m pip install --no-index --no-build-isolation --prefix=%{buildroot}%{install_path} tomli-%{tomli_version}/
python3.8 -m pip install --no-index --no-build-isolation --prefix=%{buildroot}%{install_path} packaging-%{packaging_version}/
python3.8 -m pip install --no-index --no-build-isolation --prefix=%{buildroot}%{install_path} typing_extensions-%{typing_extensions_version}/
python3.8 -m pip install --no-index --no-build-isolation --prefix=%{buildroot}%{install_path}  setuptools_scm-%{setuptools_scm_version}/

rm -r %{buildroot}%{install_path}/lib/python%{python3_version}/test
pathfix.py -pni %{install_path}/bin/python3 %{buildroot}%{install_path}

# pathfix.py won't work on wheel for some reason 
sed -i 's|%{buildroot}%{install_path}/bin/python%{python3_version}|%{install_path}/bin/python3|g' %{buildroot}%{install_path}/bin/wheel

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

prepend_path("PYTHONPATH", "%{install_path}/lib64/python%{python3_version}/site-packages")
prepend_path("PYTHONPATH", "%{install_path}/lib/python%{python3_version}/site-packages")

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
