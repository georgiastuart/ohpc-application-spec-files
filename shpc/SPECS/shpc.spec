#----------------------------------------------------------------------------bh-
# This RPM .spec file builds Singularity HPC to be compatible
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
%define pname shpc

# Dependencies
%define python_version 3.8
%define jinja2_version 3.1.2
%define markupsafe_version 2.1.1
%define spython_version 0.3.0
%define requests_version 2.28.1
%define certifi_version 2022.12.7
%define urllib3_version 1.26.13
%define idna_version 3.4
%define charset_normalizer_version 2.1.1
%define ruamel_version 0.16.10
%define ruamelyamlclib_version 0.2.7
%define jsonschema_version 4.17.3
%define hatchling_version 1.11.1
%define pathspec_version 0.10.3
%define pluggy_version 1.0.0
%define editables_version 0.3
%define fancypypi_version 22.1.0
%define vcs_version 0.3.0
%define importlib_resources_version 5.10.1
%define zipp_version 3.11.0
%define attrs_version 22.2.0
%define pkgutil_resolve_name_version 1.3.10
%define pyrsistent_version 0.19.2

Name:       %{pname}-%{compiler_family}%{PROJ_DELIM}
Version:    0.1.17
Release:    1%{?dist}
Summary:    Singularity HPC
License:    MPL-2.0
URL:        https://github.com/singularityhub/singularity-hpc

Source0:    https://github.com/singularityhub/singularity-hpc/archive/refs/tags/%{version}.tar.gz#/singularity-hpc-%{version}.tar.gz
Source1:    https://files.pythonhosted.org/packages/7a/ff/75c28576a1d900e87eb6335b063fab47a8ef3c8b4d88524c4bf78f670cce/Jinja2-%{jinja2_version}.tar.gz
Source2:    https://files.pythonhosted.org/packages/1d/97/2288fe498044284f39ab8950703e88abbac2abbdf65524d576157af70556/MarkupSafe-%{markupsafe_version}.tar.gz
Source3:    https://files.pythonhosted.org/packages/27/fc/59dff392b52d41e5c35d3d8de201007acba5f2a069f37936832762f52fa8/spython-%{spython_version}.tar.gz
Source4:    https://files.pythonhosted.org/packages/a5/61/a867851fd5ab77277495a8709ddda0861b28163c4613b011bc00228cc724/requests-%{requests_version}.tar.gz
Source5:    https://files.pythonhosted.org/packages/37/f7/2b1b0ec44fdc30a3d31dfebe52226be9ddc40cd6c0f34ffc8923ba423b69/certifi-%{certifi_version}.tar.gz
Source6:    https://files.pythonhosted.org/packages/c2/51/32da03cf19d17d46cce5c731967bf58de9bd71db3a379932f53b094deda4/urllib3-%{urllib3_version}.tar.gz
Source7:    https://files.pythonhosted.org/packages/8b/e1/43beb3d38dba6cb420cefa297822eac205a277ab43e5ba5d5c46faf96438/idna-%{idna_version}.tar.gz
Source8:    https://files.pythonhosted.org/packages/a1/34/44964211e5410b051e4b8d2869c470ae8a68ae274953b1c7de6d98bbcf94/charset-normalizer-%{charset_normalizer_version}.tar.gz
Source9:    https://github.com/commx/ruamel-yaml/archive/refs/tags/%{ruamel_version}.tar.gz#/ruamel-yaml-%{ruamel_version}.tar.gz
Source10:   https://files.pythonhosted.org/packages/d5/31/a3e6411947eb7a4f1c669f887e9e47d61a68f9d117f10c3c620296694a0b/ruamel.yaml.clib-%{ruamelyamlclib_version}.tar.gz
Source11:   https://files.pythonhosted.org/packages/36/3d/ca032d5ac064dff543aa13c984737795ac81abc9fb130cd2fcff17cfabc7/jsonschema-%{jsonschema_version}.tar.gz
Source12:   https://files.pythonhosted.org/packages/24/20/3e21d2bc57229822ac9fb9b314d7892c16f829f34a0eb247c55fc11e09a8/hatchling-%{hatchling_version}.tar.gz
Source13:   https://files.pythonhosted.org/packages/32/1a/6baf904503c3e943cae9605c9c88a43b964dea5b59785cf956091b341b08/pathspec-%{pathspec_version}.tar.gz
Source14:   https://files.pythonhosted.org/packages/a1/16/db2d7de3474b6e37cbb9c008965ee63835bba517e22cdb8c35b5116b5ce1/pluggy-%{pluggy_version}.tar.gz
Source15:   https://files.pythonhosted.org/packages/01/b0/a2a87db4b6cb8e7d57004b6836faa634e0747e3e39ded126cdbe5a33ba36/editables-%{editables_version}.tar.gz
Source16:   https://files.pythonhosted.org/packages/7a/ce/5bd1aade0bcc1b08e4968e768f04067701ca78908f8eae7c5dee99a0bf05/hatch_fancy_pypi_readme-%{fancypypi_version}.tar.gz
Source17:   https://files.pythonhosted.org/packages/04/33/b68d68e532392d938472d16a03e4ce0ccd749ea31b42d18f8baa6547cbfd/hatch_vcs-%{vcs_version}.tar.gz
Source18:   https://files.pythonhosted.org/packages/1c/c8/cfc6ae38e378be60925f121cce01e7f4996dc3aca424799a693e48c9ce4d/importlib_resources-%{importlib_resources_version}.tar.gz
Source19:   https://files.pythonhosted.org/packages/8e/b3/8b16a007184714f71157b1a71bbe632c5d66dd43bc8152b3c799b13881e1/zipp-%{zipp_version}.tar.gz
Source20:   https://files.pythonhosted.org/packages/21/31/3f468da74c7de4fcf9b25591e682856389b3400b4b62f201e65f15ea3e07/attrs-%{attrs_version}.tar.gz
Source21:   https://files.pythonhosted.org/packages/70/f2/f2891a9dc37398696ddd945012b90ef8d0a034f0012e3f83c3f7a70b0f79/pkgutil_resolve_name-%{pkgutil_resolve_name_version}.tar.gz
Source22:   https://files.pythonhosted.org/packages/b8/ef/325da441a385a8a931b3eeb70db23cb52da42799691988d8d943c5237f10/pyrsistent-%{pyrsistent_version}.tar.gz

%define install_path %{OHPC_APPS}/%{compiler_family}/%{pname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}
%define registry_path %{OHPC_PUB}/registry

BuildRequires: python38-%{compiler_family}%{PROJ_DELIM}
Requires: python38-%{compiler_family}%{PROJ_DELIM}


%description
Singularity Registry HPC (shpc) allows you to install containers as modules.

%prep
%setup -q -n singularity-hpc-%{version}

%build
#  No Build Stage

%install
module load %{compiler_family} python38

export PYTHONPATH=%{buildroot}%{install_path}/lib/python%{python_version}/site-packages:${PYTHONPATH}

# Install dependencies
python%{python_version} -m pip install \
  %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4} %{SOURCE5} %{SOURCE6} %{SOURCE7} \
  %{SOURCE8} %{SOURCE9} %{SOURCE10} %{SOURCE13} \
  %{SOURCE14} %{SOURCE15}  %{SOURCE18} %{SOURCE19} \
  %{SOURCE20} %{SOURCE21} %{SOURCE22} \
  --no-build-isolation --prefix=%{buildroot}%{install_path}
python%{python_version} -m pip install \
  %{SOURCE12} \
  --no-build-isolation --prefix=%{buildroot}%{install_path}
python%{python_version} -m pip install \
  %{SOURCE16} %{SOURCE17} \
  --no-build-isolation --prefix=%{buildroot}%{install_path}
python%{python_version} -m pip install \
  %{SOURCE11} \
  --no-build-isolation --prefix=%{buildroot}%{install_path}

# Install SHPC
python%{python_version} -m pip install . --no-build-isolation --prefix=%{buildroot}%{install_path}

# Needed to avoid mangling the templates
chmod a-x %{buildroot}/%{install_path}/lib/python%{python_version}/site-packages/shpc/main/modules/templates/test.sh
chmod a-x %{buildroot}/%{install_path}/lib/python%{python_version}/site-packages/shpc/main/wrappers/templates/bases/shell-script-base.sh

# Set the registry paths...
%{__mkdir_p} %{buildroot}%{registry_path}/registry
%{buildroot}%{install_path}/bin/shpc config add registry:%{buildroot}%{registry_path}/registry
%{buildroot}%{install_path}/bin/shpc config set module_base %{registry_path}/modules 
%{buildroot}%{install_path}/bin/shpc config set container_base %{registry_path}/containers

# ... and then edit out the buildroot
sed -i 's|%{buildroot}||g' %{buildroot}%{install_path}/lib/python%{python_version}/site-packages/shpc/settings.yml

# Module File
%{__mkdir_p}  %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}
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

prepend-path    PYTHONPATH          %{install_path}/lib/python%{python_version}/site-packages
prepend-path    PATH                %{install_path}/bin

setenv          root_dir            %{registry_path}

depends-on      python38

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/.version.%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}%{OHPC_CUSTOM_PKG_DELIM}"
EOF

%files
%{OHPC_PUB}
%dir %{registry_path}
%config %{install_path}/lib/python%{python_version}/site-packages/shpc/settings.yml


%changelog
* Thu Dec 22 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.17-1.ohpc
- Refactor to rely on OHPC compatible Python 3.8 
- Update to v0.1.17
- Remove no sha patch
* Thu Oct 13 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.14-3.ohpc
- Actually fix patch
* Thu Oct 13 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.14-2.ohpc
- Fix patch path
* Thu Oct 13 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.14-1.ohpc
- Update to 0.1.14
* Wed Oct 5 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 0.1.12-ohpc
- Initial SHPC OpenHPC RPM
