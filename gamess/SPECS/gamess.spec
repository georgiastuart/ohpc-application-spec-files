#----------------------------------------------------------------------------bh-
# This RPM .spec file builds GAMESS to be compatible
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
%define pname gamess

Name:       %{pname}-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Version:    2022.09.30.R2
Release:    1%{?dist}
Summary:    GAMESS
License:    Proprietary
URL:        https://www.msg.chem.iastate.edu/gamess

Source0:    https://www.msg.chem.iastate.edu/GAMESS/download/source/gamess-current.tar.gz
Source1:    OHPC_setup_compiler
Source2:    OHPC_setup_mpi

%define install_path %{OHPC_APPS}/%{compiler_family}/%{mpi_family}/%{pname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}

BuildRequires: python3
BuildRequires: python3-devel
BuildRequires: python3-jinja2
BuildRequires: phdf5-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
BuildRequires: boost-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
BuildRequires: globalarrays-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
BuildRequires: eigen3
BuildRequires: openblas-static
Requires: phdf5-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Requires: boost-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Requires: globalarrays-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}


%description
GAMESS is a program for ab initio molecular quantum chemistry. Briefly, GAMESS 
can compute SCF wavefunctions ranging from RHF, ROHF, UHF, GVB, and MCSCF. 
Correlation corrections to these SCF wavefunctions include Configuration 
Interaction, second order perturbation Theory, and Coupled-Cluster approaches, 
as well as the Density Functional Theory approximation. Excited states can be 
computed by CI, EOM, or TD-DFT procedures. Nuclear gradients are available, for 
automatic geometry optimization, transition state searches, or reaction path 
following. Computation of the energy hessian permits prediction of vibrational 
frequencies, with IR or Raman intensities. Solvent effects may be modeled by the
discrete Effective Fragment potentials, or continuum models such as the 
Polarizable Continuum Model. Numerous relativistic computations are available, 
including infinite order two component scalar relativity corrections, with 
various spin-orbit coupling options. The Fragment Molecular Orbital method 
permits use of many of these sophisticated treatments to be used on very large 
systems, by dividing the computation into small fragments. Nuclear wavefunctions
can also be computed, in VSCF, or with explicit treatment of nuclear orbitals by
the NEO code.


%prep
%setup -q -n %{pname}

%build
%ohpc_setup_compiler

module load phdf5
module load boost
module load globalarrays

export GMS_PATH=$PWD
%{__mkdir_p} %{buildroot}%{install_path}/ddi/

./bin/create-install-info.py --build_path %{buildroot}%{install_path} \
      --openblas \
      --mathlib_path=%{_libdir} \
      --fortran_version 9.4.0
make ddi 
make modules 
make gamess


# Module File
%{__mkdir_p} %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0##########################################################

proc ModulesHelp { } {

    puts stderr " "
    puts stderr "This module loads the %{pname} package for GAMESS (non GPU) build with %{compiler_family} and %{mpi_family} MPI."
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

depends-on      phdf5
depends-on      boost
depends-on      globalarrays

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
* Fri Dec 9 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 2022.09.30.R2-ohpc
- Initial GAMESS OpenHPC RPM
  