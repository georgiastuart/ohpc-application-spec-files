#----------------------------------------------------------------------------bh-
# This RPM .spec file builds Singularity HPC to be compatible
# with the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#----------------------------------------------------------------------------eh-

%define ohpc_compiler_dependent 0
%define ohpc_mpi_dependent 0
%define ohpc_python_dependent 0
%include %{_sourcedir}/OHPC_macros

# Base package name
%define pname shpc

Name:       %{pname}%{PROJ_DELIM}
Version:    0.1.14
Release:    3%{?dist}
Summary:    Singularity HPC
License:    MPL-2.0
URL:        https://github.com/singularityhub/singularity-hpc

Source0:    https://github.com/singularityhub/singularity-hpc/archive/refs/tags/%{version}.tar.gz

Patch0:     nosha.patch

%define install_path %{OHPC_APPS}/%{pname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}
%define registry_path %{OHPC_PUB}/registry

BuildRequires: python38
BuildRequires: python38-pip
Requires: python38


%description
Singularity Registry HPC (shpc) allows you to install containers as modules.


%prep
%setup -q -n singularity-hpc-%{version}
%patch0 -p1


%build
#  No Build Stage

%install
export PYTHONPATH=%{buildroot}%{install_path}/lib/python3.8/site-packages:${PYTHONPATH}
python3.8 setup.py install --prefix=%{buildroot}%{install_path} --install-scripts=%{buildroot}%{install_path}/bin
# Needed to avoid mangling the templates
chmod a-x %{buildroot}/%{install_path}/lib/python3.8/site-packages/singularity_hpc-%{version}-py3.8.egg/shpc/main/modules/templates/test.sh
chmod a-x %{buildroot}/%{install_path}/lib/python3.8/site-packages/singularity_hpc-%{version}-py3.8.egg/shpc/main/wrappers/templates/bases/shell-script-base.sh

%{__mkdir_p} %{buildroot}/%{registry_path}/registry

# Module File
%{__mkdir_p} %{buildroot}/%{OHPC_MODULES}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0##########################################################

proc ModulesHelp { } {

    puts stderr " "
    puts stderr "This module loads the %{pname} package for the Singularity HPC."
    puts stderr "\nVersion %{version}\n"
    puts stderr " "

}

module-whatis "Name: Singularity HPC"
module-whatis "Version: %{version}"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set             version             %{version}

prepend-path    PYTHONPATH          %{install_path}/lib/python3.8/site-packages
prepend-path    PATH                %{install_path}/bin

setenv          root_dir            %{registry_path}

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULES}/%{pname}/.version.%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}%{OHPC_CUSTOM_PKG_DELIM}"
EOF

%post 
export PYTHONPATH=%{install_path}/lib/python3.8/site-packages:${PYTHONPATH}
%{install_path}/bin/shpc config add registry:%{registry_path}/registry
%{install_path}/bin/shpc config set module_base %{registry_path}/modules 
%{install_path}/bin/shpc config set container_base %{registry_path}/containers

%files
%{OHPC_PUB}
%dir %{registry_path}
%config %{install_path}/lib/python3.8/site-packages/singularity_hpc-%{version}-py3.8.egg/shpc/settings.yml


%changelog
* Thu Oct 13 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.14-3.ohpc
- Actually fix patch
* Thu Oct 13 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.14-2.ohpc
- Fix patch path
* Thu Oct 13 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.14-1.ohpc
- Update to 0.1.14
* Wed Oct 5 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.12-ohpc
- Initial SHPC OpenHPC RPM
