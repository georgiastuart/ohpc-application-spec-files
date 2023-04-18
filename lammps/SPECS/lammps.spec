#----------------------------------------------------------------------------bh-
# This RPM .spec file builds LAMMPS to be compatible
# with the OpenHPC project.
#
# It may have been modified from the default version supplied by the underlying
# release package (if available) in order to apply patches, perform customized
# build/install configurations, and supply additional files to support
# desired integration conventions.
#
#----------------------------------------------------------------------------eh-

%define ohpc_compiler_dependent 1
%define ohpc_mpi_dependent 1
%define ohpc_python_dependent 0
%include %{_sourcedir}/OHPC_macros

# Base package name
%define pname lammps

Name:       %{pname}-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Version:    23Jun2022
Release:    1%{?dist}
Summary:    LAMMPS
License:    GPLv2
URL:        https://www.lammps.org/

Source0:    https://download.lammps.org/tars/lammps-stable.tar.gz
Source1:    OHPC_setup_compiler
Source2:    OHPC_setup_mpi

%define install_path %{OHPC_APPS}/%{compiler_family}/%{mpi_family}/%{pname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}

BuildRequires: cmake-ohpc
BuildRequires: fftw-%{compiler_family}-%{mpi_family}-ohpc
BuildRequires: libpng-devel
BuildRequires: openblas-%{compiler_family}-ohpc


%description
LAMMPS is a classical molecular dynamics code with a focus on materials
modeling. It's an acronym for Large-scale Atomic/Molecular Massively
Parallel Simulator.

LAMMPS has potentials for solid-state materials (metals, semiconductors)
and soft matter (biomolecules, polymers) and coarse-grained or mesoscopic
systems. It can be used to model atoms or, more generically, as a parallel
particle simulator at the atomic, meso, or continuum scale.


%prep
%setup -q -n %{pname}-%{version}

%build
%ohpc_setup_compiler

module load %{compiler_family}
module load %{mpi_family}
module load openblas
module load cmake

mkdir build; cd build
cmake -DCMAKE_INSTALL_PREFIX=%{buildroot}%{install_path} ../cmake
make -j 8
make install

# Module File
%{__mkdir_p} %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0##########################################################

proc ModulesHelp { } {

    puts stderr " "
    puts stderr "This module loads the %{pname} package for LAMMPS built with %{compiler_family} and %{mpi_family} MPI."
    puts stderr "\nVersion %{version}\n"
    puts stderr " "

}

module-whatis "Name: %{PNAME} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set     version                     %{version}

prepend-path    PATH                %{install_path}

setenv          %{PNAME}_DIR        %{install_path}

depends-on      openblas

EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/.version.%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}%{OHPC_CUSTOM_PKG_DELIM}"
EOF


%files
%{OHPC_PUB}


%changelog
* Tue Apr 18 2023 Sol Jerome <solj@utdallas.edu> - 23Jun2022-ohpc
- Initial LAMMPS OpenHPC RPM
