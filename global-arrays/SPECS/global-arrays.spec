#----------------------------------------------------------------------------bh-
# This RPM .spec file builds Global Arrays to be compatible
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
%define pname globalarrays

Name:       %{pname}-%{compiler_family}-%{mpi_family}%{PROJ_DELIM}
Version:    5.8.2
Release:    1%{?dist}
Summary:    GlobalArrays
License:    BSD-3-Clause
URL:        https://www.msg.chem.iastate.edu/gamess

# Conda Sources (one digit)
Source0:    https://github.com/GlobalArrays/ga/releases/download/v%{version}/ga-%{version}.tar.gz
Source1:    OHPC_setup_compiler
Source2:    OHPC_setup_mpi

%define install_path %{OHPC_APPS}/%{compiler_family}/%{mpi_family}/%{pname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}

BuildRequires: openssh-clients
Requires: openssh-clients

%description
Global Arrays (GA) is a Partitioned Global Address Space (PGAS) programming 
model. It provides primitives for one-sided communication (Get, Put, Accumulate)
and Atomic Operations (read increment). It supports blocking and non-blocking
primtives, and supports location consistency.

%prep
%setup -q -n ga-%{version}

%build
%ohpc_setup_compiler

./configure --with-mpi --prefix=%{install_path}
make 

%install
make DESTDIR=%{buildroot} install


# Module File
%{__mkdir_p} %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}-%{mpi_family}/%{pname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0##########################################################

proc ModulesHelp { } {

    puts stderr " "
    puts stderr "This module loads the %{pname} package for GlobalArray (non GPU) build with %{compiler_family} and %{mpi_family} MPI."
    puts stderr "\nVersion %{version}\n"
    puts stderr " "

}

module-whatis "Name: %{PNAME} built with %{compiler_family} compiler and %{mpi_family} MPI"
module-whatis "Version: %{version}"
module-whatis "Description: %{summary}"
module-whatis "URL %{url}"

set     version                     %{version}


prepend-path    PATH                %{install_path}/bin
prepend-path    INCLUDE             %{install_path}/include
prepend-path    LD_LIBRARY_PATH     %{install_path}/lib

setenv          %{PNAME}_DIR        %{install_path}
setenv          %{PNAME}_BIN        %{install_path}/bin
setenv          %{PNAME}_LIB        %{install_path}/lib
setenv          %{PNAME}_INC        %{install_path}/include

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
* Fri Dec 9 2022 Georgia Stuart <georgia.stuart@utdallas.edu> - 5.8.2-ohpc
- Initial GlobalArray OpenHPC RPM
  