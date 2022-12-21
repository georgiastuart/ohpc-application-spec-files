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
%define tqdm_version 4.64.1
%define requests_version 2.28.1
%define certifi_version 2022.12.7
%define urllib3_version 1.26.13
%define idna_version 3.4
%define charset_normalizer_version 2.1.1

Name:       %{pname}%{PROJ_DELIM}
Version:    22.11.1
Release:    3%{?dist}
Summary:    Conda Package Manager
License:    BSD 3-Clause
URL:        https://github.com/conda/conda

Source0:   https://github.com/conda/conda/archive/refs/tags/%{version}.tar.gz#/conda-%{version}.tar.gz
Source1:   https://files.pythonhosted.org/packages/a1/16/db2d7de3474b6e37cbb9c008965ee63835bba517e22cdb8c35b5116b5ce1/pluggy-%{pluggy_version}.tar.gz
Source2:   https://github.com/conda/pycosat/archive/refs/tags/%{pycosat_version}.tar.gz#/pycosat-%{pycosat_version}.tar.gz
Source3:   https://github.com/commx/ruamel-yaml/archive/refs/tags/%{ruamel_version}.tar.gz#/ruamel-yaml-%{ruamel_version}.tar.gz
Source4:   https://files.pythonhosted.org/packages/c1/c2/d8a40e5363fb01806870e444fc1d066282743292ff32a9da54af51ce36a2/tqdm-%{tqdm_version}.tar.gz
Source5:   https://anaconda.org/anaconda/conda-package-handling/%{conda_package_handling_version}/download/linux-64/conda-package-handling-%{conda_package_handling_version}-py38h5eee18b_1.tar.bz2
Source6:   https://files.pythonhosted.org/packages/d5/31/a3e6411947eb7a4f1c669f887e9e47d61a68f9d117f10c3c620296694a0b/ruamel.yaml.clib-%{ruamelyamlclib_version}.tar.gz
Source7:   https://files.pythonhosted.org/packages/a5/61/a867851fd5ab77277495a8709ddda0861b28163c4613b011bc00228cc724/requests-%{requests_version}.tar.gz
Source8:   https://files.pythonhosted.org/packages/37/f7/2b1b0ec44fdc30a3d31dfebe52226be9ddc40cd6c0f34ffc8923ba423b69/certifi-%{certifi_version}.tar.gz
Source9:   https://files.pythonhosted.org/packages/c2/51/32da03cf19d17d46cce5c731967bf58de9bd71db3a379932f53b094deda4/urllib3-%{urllib3_version}.tar.gz
Source10:  https://files.pythonhosted.org/packages/8b/e1/43beb3d38dba6cb420cefa297822eac205a277ab43e5ba5d5c46faf96438/idna-%{idna_version}.tar.gz
Source11:  https://files.pythonhosted.org/packages/a1/34/44964211e5410b051e4b8d2869c470ae8a68ae274953b1c7de6d98bbcf94/charset-normalizer-%{charset_normalizer_version}.tar.gz

Patch0:     %{pname}-no_system_prefix.patch
Patch1:     %{pname}-entrypoint.patch

%define install_path %{OHPC_APPS}/%{pname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}

BuildRequires: python38-%{compiler_family}%{PROJ_DELIM}
Requires: python38-%{compiler_family}%{PROJ_DELIM}


%description
Conda is a cross-platform, language-agnostic binary package manager. It is the
package manager used by Anaconda installations, but it may be
used for other systems as well.  Conda makes environments first-class
citizens, making it easy to create independent environments even for C
libraries. Conda is written entirely in Python, and is BSD licensed open
source.


%prep
%setup -q -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -a 9 -a 10 -a 11 -n %{pname}-%{version}
%patch0 -p0
%patch1 -p0

# Set the version for setup.py
sed -r -i 's/^(__version__ = ).*/\1"%{version}"/' conda/__init__.py

%build
#  No Build Stage

%install
module load gnu9 python38

%{__mkdir_p} %{buildroot}/%{install_path}

export PYTHONPATH="%{buildroot}/%{install_path}/lib64/python%{python3_version}/site-packages:%{buildroot}/%{install_path}/lib/python%{python3_version}/site-packages:$PYTHONPATH"
export CONDA_ROOT="%{buildroot}/%{install_path}"

# Install required packages
python3.8 -m pip install pluggy-%{pluggy_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 
python3.8 -m pip install pycosat-%{pycosat_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 
python3.8 -m pip install ruamel.yaml.clib-%{ruamelyamlclib_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 
python3.8 -m pip install ruamel-yaml-%{ruamel_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 
python3.8 -m pip install tqdm-%{tqdm_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 
python3.8 -m pip install certifi-%{certifi_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}"
python3.8 -m pip install urllib3-%{urllib3_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}"  
python3.8 -m pip install idna-%{idna_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 
python3.8 -m pip install charset-normalizer-%{charset_normalizer_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 
python3.8 -m pip install requests-%{requests_version}/ --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 

# Install conda
python3.8 -m pip install . --no-deps --no-build-isolation --prefix="%{buildroot}%{install_path}" 

# Install conda_package_handling and six
%{__mkdir_p} conda_package_handling
tar xvf %{SOURCE5} -C conda_package_handling
%{__cp} -r conda_package_handling/lib/python%{python3_version}/site-packages/conda_package_handling %{buildroot}/%{install_path}/lib/python%{python3_version}/site-packages/

# Set up source files
# TODO: FIX csh FILE
%{__mkdir_p} %{buildroot}/%{install_path}/etc/profile.d
install -m 0644 -Dt %{buildroot}/%{install_path}/etc/profile.d/ conda/shell/etc/profile.d/conda.{sh,csh}
sed -i '1s|^|export CONDA_EXE="%{install_path}/bin/conda"\nexport _CE_M=""\nexport _CE_CONDA=""\nexport CONDA_PYTHON_EXE="/opt/ohpc/pub/apps/gnu9/python38/3.8.15/bin/python3.8"\n\n|' %{buildroot}/%{install_path}/etc/profile.d/conda.sh

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
prepend_path("PYTHONPATH", "%{install_path}/lib64/python%{python3_version}/site-packages")

setenv("%{PNAME}_ROOT", "%{install_path}")

source_sh("bash", "%{install_path}/etc/profile.d/conda.sh")
-- TODO: Figure out other shells
-- source_sh("dash", "%{install_path}/etc/profile.d/conda.sh")
-- source_sh("zsh", "%{install_path}/etc/profile.d/conda.sh")
-- source_sh("csh", "%{install_path}/etc/profile.d/conda.csh")
-- source_sh("tcsh", "%{install_path}/etc/profile.d/conda.csh")

depends_on('python38')

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/.version.%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}%{OHPC_CUSTOM_PKG_DELIM}"
EOF

%files
%{OHPC_PUB}
%doc README.md
%license LICENSE.txt


%changelog
* Wed Dec 21 2022 Georgia Stuart <georgia.stuart@utdallas.edu> 22.11.1-3.ohpc
- Refactor out python and setuptools dependencies to rely on python38-ohpc
- Refactor to only use pip install 
- Add conda env entrypoint
* Tue Dec 20 2022 Sol Jerome <solj@utdallas.edu> - 22.11.1-2.ohpc
- Fix building without network
- Add package name prefix to patches
* Sun Dec 18 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 22.11.1-ohpc
- Update to 22.11.1
- Remove venv workaround
* Wed Jan 26 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 4.11.0-ohpc
- Initial Conda OpenHPC RPM
