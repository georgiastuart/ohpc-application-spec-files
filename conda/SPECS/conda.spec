#----------------------------------------------------------------------------bh-
# This RPM .spec file builds Conda Package Manager to be compatible
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

%define ohpc_compiler_dependent 0
%define ohpc_mpi_dependent 0
%define ohpc_python_dependent 0
%include %{_sourcedir}/OHPC_macros

# Base package name
%define pname conda
%define conda_package_handling_version 1.9.0
%define pluggy_version 1.0.0
%define pycosat_version 0.6.4
%define python3_version 3.8
%define ruamel_version 0.16.10
%define ruamelyamlclib_version 0.2.7
%define setuptools_version 65.6.3
%define tqdm_version 4.64.1

Name:       %{pname}%{PROJ_DELIM}
Version:    22.11.1
Release:    2%{?dist}
Summary:    Conda Package Manager
License:    BSD 3-Clause
URL:        https://github.com/conda/conda

Source0:   https://github.com/conda/conda/archive/refs/tags/%{version}.tar.gz
Source1:   https://files.pythonhosted.org/packages/a1/16/db2d7de3474b6e37cbb9c008965ee63835bba517e22cdb8c35b5116b5ce1/pluggy-%{pluggy_version}.tar.gz
Source2:   https://github.com/conda/pycosat/archive/refs/tags/%{pycosat_version}.tar.gz#/pycosat-%{pycosat_version}.tar.gz
Source3:   https://github.com/commx/ruamel-yaml/archive/refs/tags/%{ruamel_version}.tar.gz#/ruamel-yaml-%{ruamel_version}.tar.gz
Source4:   https://files.pythonhosted.org/packages/c1/c2/d8a40e5363fb01806870e444fc1d066282743292ff32a9da54af51ce36a2/tqdm-%{tqdm_version}.tar.gz
Source5:   https://files.pythonhosted.org/packages/b6/21/cb9a8d0b2c8597c83fce8e9c02884bce3d4951e41e807fc35791c6b23d9a/setuptools-%{setuptools_version}.tar.gz
Source6:   https://anaconda.org/anaconda/conda-package-handling/%{conda_package_handling_version}/download/linux-64/conda-package-handling-%{conda_package_handling_version}-py38h5eee18b_1.tar.bz2
Source7:   https://files.pythonhosted.org/packages/d5/31/a3e6411947eb7a4f1c669f887e9e47d61a68f9d117f10c3c620296694a0b/ruamel.yaml.clib-%{ruamelyamlclib_version}.tar.gz

Patch0:     %{pname}-no_system_prefix.patch
Patch1:     %{pname}-entrypoint.patch

%define install_path %{OHPC_APPS}/%{pname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}

BuildRequires: python38-devel
BuildRequires: python38-pip
BuildRequires: python38-requests
BuildRequires: python38-setuptools_scm
BuildRequires: python38-toml
Requires: python38
Requires: python38-requests


%description
Conda is a cross-platform, language-agnostic binary package manager. It is the
package manager used by Anaconda installations, but it may be
used for other systems as well.  Conda makes environments first-class
citizens, making it easy to create independent environments even for C
libraries. Conda is written entirely in Python, and is BSD licensed open
source.


%prep
%setup -q -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -n %{pname}-%{version}
%patch0 -p0
%patch1 -p0

# Set the version for setup.py
sed -r -i 's/^(__version__ = ).*/\1"%{version}"/' conda/__init__.py

%build
#  No Build Stage

%install
%{__mkdir_p} %{buildroot}/%{install_path}

export PYTHONPATH="%{buildroot}/%{install_path}/lib64/python%{python3_version}/site-packages:%{buildroot}/%{install_path}/lib/python%{python3_version}/site-packages:$PYTHONPATH"
export CONDA_ROOT="%{buildroot}/%{install_path}"

# Install required packages
(cd setuptools-%{setuptools_version} && python3.8 setup.py install --prefix=%{buildroot}%{install_path} --install-scripts=%{buildroot}%{install_path}/bin)
(cd pluggy-%{pluggy_version} && python3.8 setup.py install --prefix=%{buildroot}%{install_path} --install-scripts=%{buildroot}%{install_path}/bin)
(cd pycosat-%{pycosat_version} && python3.8 setup.py install --prefix=%{buildroot}%{install_path} --install-scripts=%{buildroot}%{install_path}/bin)
pip3.8 install ruamel.yaml.clib-%{ruamelyamlclib_version}/ --no-deps --install-option="--prefix=%{buildroot}%{install_path}" --install-option="--install-scripts=%{buildroot}%{install_path}/bin"
pip3.8 install ruamel-yaml-%{ruamel_version}/ --no-deps --install-option="--prefix=%{buildroot}%{install_path}" --install-option="--install-scripts=%{buildroot}%{install_path}/bin"
(cd tqdm-%{tqdm_version} && python3.8 setup.py install --prefix=%{buildroot}%{install_path} --install-scripts=%{buildroot}%{install_path}/bin)

# Install conda
python3.8 setup.py install --prefix=%{buildroot}%{install_path} --install-scripts=%{buildroot}%{install_path}/bin

# Install conda_package_handling and six
%{__mkdir_p} conda_package_handling
tar xvf %{SOURCE6} -C conda_package_handling
%{__cp} -r conda_package_handling/lib/python%{python3_version}/site-packages/conda_package_handling %{buildroot}/%{install_path}/lib/python%{python3_version}/site-packages/

# Set up source files
# TODO: FIX csh FILE
%{__mkdir_p} %{buildroot}/%{install_path}/etc/profile.d
install -m 0644 -Dt %{buildroot}/%{install_path}/etc/profile.d/ conda/shell/etc/profile.d/conda.{sh,csh}
sed -i '1s|^|export CONDA_EXE="%{install_path}/bin/conda"\nexport _CE_M=""\nexport _CE_CONDA=""\nexport CONDA_PYTHON_EXE="/usr/bin/python%{python3_version}"\n\n|' %{buildroot}/%{install_path}/etc/profile.d/conda.sh

#  Modified from https://src.fedoraproject.org/rpms/conda/blob/rawhide/f/conda.spec
%{__mkdir_p} %{buildroot}%{install_path}/condarc.d
%{__cat} << EOF > %{buildroot}%{install_path}/condarc.d/defaults.yaml
root_prefix: %{install_path}
pkgs_dirs:
 - ~/.conda/pkgs
 - %{install_path}/pkgs
envs_dirs:
 - ~/.conda/envs
 - %{install_path}/envs
auto_activate_base: false
EOF

%{__cat} << EOF > %{buildroot}%{install_path}/.condarc
root_prefix: %{install_path}
pkgs_dirs:
 - ~/.conda/pkgs
 - %{install_path}/pkgs
envs_dirs:
 - ~/.conda/envs
 - %{install_path}/envs
auto_activate_base: false
EOF

# Module File
%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}.lua
help([[
This module loads the %{pname} package for the Conda package and environment
manager.

Version %{version}
]])

whatis("Name: Conda Package Manager")
whatis("Version: %{version}")
whatis("Description: %{summary}")
whatis("URL: %{url}")

local version = "%{version}"

prepend_path("PYTHONPATH", "%{install_path}/lib/python%{python3_version}/site-packages")

setenv("%{PNAME}_ROOT", "%{install_path}")

source_sh("bash", "%{install_path}/etc/profile.d/conda.sh")
-- TODO: Figure out other shells
-- source_sh("dash", "%{install_path}/etc/profile.d/conda.sh")
-- source_sh("zsh", "%{install_path}/etc/profile.d/conda.sh")
-- source_sh("csh", "%{install_path}/etc/profile.d/conda.csh")
-- source_sh("tcsh", "%{install_path}/etc/profile.d/conda.csh")

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/.version.%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}%{OHPC_CUSTOM_PKG_DELIM}"
EOF

# THIS IS COMMENTED OUT DUE TO AN ISSUE WITH source-sh AND OPENHPC LMOD
# SEE ABOVE FOR LUA FILE

# # Module File
# %{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/.%{pname}
# %{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/.%{pname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}
# #%Module4.6##########################################################

# proc ModulesHelp { } {

#     puts stderr " "
#     puts stderr "This module loads the %{pname} package for the Conda package and environment manager."
#     puts stderr "\nVersion %{version}\n"
#     puts stderr " "

# }

# module-whatis "Name: Conda Package Manager"
# module-whatis "Version: %{version}"
# module-whatis "Description: %{summary}"
# module-whatis "URL %{url}"

# set             version             %{version}


# prepend-path    PATH                %{install_path}/condabin
# prepend-path    PATH                %{install_path}/lib/python%{python3_version}/site-packages/conda-%{version}-py%{python3_version}.egg/conda/shell/bin
# prepend-path    PYTHONPATH          %{install_path}/lib/python%{python3_version}/site-packages

# setenv          %{PNAME}_DIR        %{install_path}
# setenv          %{PNAME}_BIN        %{install_path}/condabin
# setenv          %{PNAME}_LIB        %{install_path}/lib
# setenv          CONDA_ROOT          %{install_path}
# setenv          CONDA_ROOT_PREFIX   %{install_path}
# setenv          _CONDA_ROOT         %{install_path}
# setenv          CONDA_EXE           %{install_path}/condabin/conda

# source-sh       bash                %{install_path}/etc/profile.d/conda.sh
# # source-sh       dash                %{install_path}/etc/profile.d/conda.sh
# # source-sh       zsh                 %{install_path}/etc/profile.d/conda.sh
# # source-sh       csh                 %{install_path}/etc/profile.d/conda.csh
# # source-sh       tcsh                %{install_path}/etc/profile.d/conda.csh

# EOF

# %{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/.%{pname}/.version.%{version}%{OHPC_CUSTOM_PKG_DELIM}
# #%Module1.0#####################################################################
# ##
# ## version file for %{pname}-%{version}
# ##
# set     ModulesVersion      "%{version}%{OHPC_CUSTOM_PKG_DELIM}"
# EOF



%files
%{OHPC_PUB}
%doc README.md
%license LICENSE.txt


%changelog
* Tue Dec 20 2022 Sol Jerome <solj@utdallas.edu> - 22.11.1-2.ohpc
- Fix building without network
- Add package name prefix to patches
* Sun Dec 18 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 22.11.1-ohpc
- Update to 22.11.1
- Remove venv workaround
* Wed Jan 26 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 4.11.0-ohpc
- Initial Conda OpenHPC RPM
