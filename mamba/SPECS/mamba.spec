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
%define pname mamba

# Dependency versions
%define nlohmann_json_version 3.11.2
%define pybind11_version 2.10.1
%define reproc_version 14.2.4
%define expected_version 1.0.0
%define termcolor_version 2.1.0
%define curl_version 7.86.0
%define libsolv_version 0.7.23
%define spdlog_version 1.11.0
%define fmt_version 9.1.0
%define conda_version 22.11.1

# Mamba maintainers label the source code with date, not version :(
%define date 2022.11.01

Name:       %{pname}-%{compiler_family}%{PROJ_DELIM}
Version:    1.0.0
Release:    3%{?dist}
Summary:    Mamba Package Manager
License:    BSD-3-Clause
URL:        https://github.com/mamba-org/mamba
Source0:    https://github.com/mamba-org/mamba/archive/refs/tags/%{date}.tar.gz#/mamba-%{date}.tar.gz
Source1:    https://github.com/nlohmann/json/releases/download/v%{nlohmann_json_version}/json.tar.xz
Source2:    https://github.com/pybind/pybind11/archive/refs/tags/v%{pybind11_version}.tar.gz#/pybind11-%{pybind11_version}.tar.gz
Source3:    https://github.com/DaanDeMeyer/reproc/archive/refs/tags/v%{reproc_version}.tar.gz#/reproc-%{reproc_version}.tar.gz
Source4:    https://github.com/TartanLlama/expected/archive/refs/tags/v%{expected_version}.tar.gz#/expected-%{expected_version}.tar.gz
Source5:    https://github.com/ikalnytskyi/termcolor/archive/refs/tags/v%{termcolor_version}.tar.gz#/termcolor-%{termcolor_version}.tar.gz
Source6:    https://github.com/curl/curl/releases/download/curl-7_86_0/curl-%{curl_version}.tar.bz2
Source7:    https://github.com/openSUSE/libsolv/archive/refs/tags/%{libsolv_version}.tar.gz#/libsolve-%{libsolv_version}.tar.gz
Source8:    https://github.com/gabime/spdlog/archive/refs/tags/v%{spdlog_version}.tar.gz#/spdlog-%{spdlog_version}.tar.gz
Source9:    https://github.com/fmtlib/fmt/archive/refs/tags/%{fmt_version}.tar.gz#/fmt-%{fmt_version}.tar.gz
Source10:   https://raw.githubusercontent.com/TartanLlama/tl-cmake/master/add-tl.cmake
Source11:   OHPC_setup_compiler


Patch0:     lib_path.patch
Patch1:     0001-dont-fetch-from-git.patch

%define install_path %{OHPC_APPS}/%{compiler_family}/%{pname}%{OHPC_CUSTOM_PKG_DELIM}/%{version}

BuildRequires: python38-%{compiler_family}%{PROJ_DELIM}
BuildRequires: cmake
BuildRequires: ninja-build
BuildRequires: libarchive-devel
BuildRequires: libsodium-devel
BuildRequires: gtest-devel
BuildRequires: gmock-devel
BuildRequires: yaml-cpp-devel
BuildRequires: cli11-devel
BuildRequires: openssl-devel
BuildRequires: git
BuildRequires: patchelf
Requires: python38-%{compiler_family}%{PROJ_DELIM}
Requires: openssl
Requires: libarchive
Requires: libsodium
Requires: conda%{PROJ_DELIM}


%description
Mamba is a reimplementation of the conda package manager in C++.


%prep
%setup -q -a 1 -a 2 -a 3 -a 4 -a 5 -a 6 -a 7 -a 8 -a 9 -n %{pname}-%{date}
%patch0 -p0
%patch1 -p0
cp %SOURCE10 expected-%{expected_version}

%build
%ohpc_setup_compiler

module load python38

cd reproc-%{reproc_version}

cmake -B build \
  -DREPROC++=ON \
  -DBUILD_SHARED_LIBS=ON \
  -DCMAKE_INSTALL_PREFIX=%{install_path}/reproc
cmake --build build
make DESTDIR=%{buildroot} install -C build/

cd ../expected-%{expected_version}

cmake -B build \
  -DEXPECTED_BUILD_TESTS=OFF \
  -DCMAKE_INSTALL_PREFIX=../expected
cmake --build build
make install -C build/

cd ../json

cmake -B build \
  -DCMAKE_INSTALL_PREFIX=../nljson \
  -DJSON_BuildTests=OFF
cmake --build build
make install -C build/

cd ../pybind11-%{pybind11_version}

cmake -B build \
  -DPYBIND11_TEST=OFF \
  -DCMAKE_INSTALL_PREFIX=../pybind11
cmake --build build
make install -C build/

cd ../spdlog-%{spdlog_version}

cmake -B build \
  -DCMAKE_INSTALL_PREFIX=%{install_path}/spdlog \
  -DSPDLOG_BUILD_SHARED=ON
cmake --build build
make DESTDIR=%{buildroot} install -C build/

cd ../curl-%{curl_version}

cmake -B build \
  -DCMAKE_INSTALL_PREFIX=%{install_path}/curl \
  -DBUILD_SHARED_LIBS=ON
cmake --build build
make DESTDIR=%{buildroot} install -C build/

cd ../libsolv-%{libsolv_version}

cmake -B build \
  -DCMAKE_INSTALL_PREFIX=%{install_path}/libsolv \
  -DENABLE_CONDA=ON
cmake --build build
make DESTDIR=%{buildroot} install -C build/

cd ../fmt-%{fmt_version}

cmake -B build \
  -DCMAKE_INSTALL_PREFIX=%{install_path}/fmt \
  -DFMT_TEST=OFF \
  -DFMT_DOC=OFF \
  -DBUILD_SHARED_LIBS=ON
cmake --build build
make DESTDIR=%{buildroot} install -C build/

cd ..

export CPLUS_INCLUDE_PATH=$PWD/json/single_include:$PWD/termcolor-%{termcolor_version}/include:%{buildroot}%{install_path}/curl/include:%{buildroot}%{install_path}/libsolv/include:%{buildroot}%{install_path}/spdlog/include:%{buildroot}%{install_path}/fmt/include:$CPLUS_INCLUDE_PATH
export LD_LIBRARY_PATH=%{buildroot}%{install_path}/libmamba/lib64:%{buildroot}%{install_path}/libsolv/lib64:%{buildroot}%{install_path}/curl/lib64:%{buildroot}%{install_path}/spdlog/lib64:%{buildroot}%{install_path}/fmt/lib64:$LD_LIBRARY_PATH

cmake -B build/ \
  -DCMAKE_INSTALL_PREFIX=%{install_path}/libmamba \
  -DCMAKE_PREFIX_PATH="%{buildroot}%{install_path}/libmamba;$PWD/nljson;%{buildroot}%{install_path}/reproc;$PWD/expected;$PWD/pybind11;%{buildroot}%{install_path}/spdlog;%{buildroot}%{install_path}/curl;%{buildroot}%{install_path}/libsolv;%{buildroot}%{install_path}/fmt" \
  -DCMAKE_CXX_FLAGS="-s" \
  -DBUILD_LIBMAMBA=ON \
  -DBUILD_SHARED=ON \
  -DBUILD_LIBMAMBAPY=ON \
  -DCMAKE_BUILD_TYPE=Release

cmake --build build/


%install
%ohpc_setup_compiler

module load python38

make DESTDIR=%{buildroot} install -C reproc-%{reproc_version}/build
make DESTDIR=%{buildroot} install -C spdlog-%{spdlog_version}/build
make DESTDIR=%{buildroot} install -C curl-%{curl_version}/build
make DESTDIR=%{buildroot} install -C libsolv-%{libsolv_version}/build
make DESTDIR=%{buildroot} install -C fmt-%{fmt_version}/build

make DESTDIR=%{buildroot} install -C build/
mv %{buildroot}$PWD/libmambapy/libmambapy/bindings.cpython-38-x86_64-linux-gnu.so $PWD/libmambapy/libmambapy/
export LD_LIBRARY_PATH=%{buildroot}%{install_path}/libmamba/lib64:%{buildroot}%{install_path}/libsolv/lib64:%{buildroot}%{install_path}/curl/lib64:%{buildroot}%{install_path}/spdlog/lib64:%{buildroot}%{install_path}/fmt/lib64:%{buildroot}%{install_path}/reproc/lib64:$LD_LIBRARY_PATH

pip3.8 install libmambapy/ --no-deps --prefix="%{buildroot}%{install_path}/libmambapy"
pip3.8 install mamba/ --no-deps --prefix="%{buildroot}%{install_path}/mamba"

# Remove buildroot from cmake targets
sed -i 's|%{buildroot}||g' %{buildroot}%{install_path}/libmamba/lib64/cmake/libmamba/libmambaTargets.cmake
patchelf --set-rpath '%{install_path}/reproc/lib64:%{install_path}/curl/lib64:%{install_path}/libsolv/lib64:%{install_path}/fmt/lib64:%{install_path}/spdlog/lib64:' %{buildroot}%{install_path}/libmamba/lib64/libmamba.so
patchelf --set-rpath '%{install_path}/reproc/lib64:%{install_path}/curl/lib64:%{install_path}/libsolv/lib64:%{install_path}/fmt/lib64:%{install_path}/spdlog/lib64:' %{buildroot}%{install_path}/libmambapy/lib/python3.8/site-packages/libmambapy/bindings.cpython-38-x86_64-linux-gnu.so

# Make it so mamba doesn't try to find itself via conda_exe
sed -i 's|$(\\dirname "${CONDA_EXE}")/mamba|%{install_path}/mamba/bin/mamba|' %{buildroot}%{install_path}/mamba/etc/profile.d/mamba.sh

# Module File
%{__mkdir_p}  %{buildroot}%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/%{version}%{OHPC_CUSTOM_PKG_DELIM}.lua
help([[
  This module loads the %{pname} package for the Mamba package and environment
  manager.

  Version %{version}
]])

whatis("Name: Mamba Package Manager")
whatis("Version: %{version}")
whatis("Description: %{summary}")
whatis("URL: %{url}")

local version = "%{version}"

prepend_path("PYTHONPATH", "%{install_path}/libmambapy/lib/python3.8/site-packages")
prepend_path("PYTHONPATH", "%{install_path}/mamba/lib/python3.8/site-packages")
prepend_path("LD_LIBRARY_PATH", "%{install_path}/libmamba/lib64")

setenv("%{PNAME}_ROOT", "%{install_path}")

source_sh("bash", "%{install_path}/mamba/etc/profile.d/mamba.sh")
-- TODO: Figure out other shells
-- source_sh("dash", "%{install_path}/etc/profile.d/conda.sh")
-- source_sh("zsh", "%{install_path}/etc/profile.d/conda.sh")
-- source_sh("csh", "%{install_path}/etc/profile.d/conda.csh")
-- source_sh("tcsh", "%{install_path}/etc/profile.d/conda.csh")

depends_on("python38")
depends_on("conda")
EOF
# #%Module1.0##########################################################

# proc ModulesHelp { } {

#     puts stderr " "
#     puts stderr "This module loads the %{pname} package for Mamba"
#     puts stderr "\nVersion %{version}\n"
#     puts stderr " "

# }

# module-whatis "Name: Mamba"
# module-whatis "Version: %{version}"
# module-whatis "Keywords: Mamba"
# module-whatis "Description: %{summary}"
# module-whatis "URL %{url}"

# set     version                     %{version}


# prepend-path    PATH                %{install_path}/bin
# prepend-path    LD_LIBRARY_PATH     %{install_path}/libmamba/lib64
# prepend-path    PYTHONPATH          %{install_path}/libmambapy/lib/python3.8/site-packages
# prepend-path    PYTHONPATH          %{install_path}/mamba/lib/python3.8/site-packages

# setenv          %{PNAME}_DIR        %{install_path}
# setenv          %{PNAME}_BIN        %{install_path}/bin

# depends-on      conda/%{conda_version}

# EOF

%{__cat} << EOF > %{buildroot}/%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}/.version.%{version}%{OHPC_CUSTOM_PKG_DELIM}
#%Module1.0#####################################################################
##
## version file for %{pname}-%{version}
##
set     ModulesVersion      "%{version}%{OHPC_CUSTOM_PKG_DELIM}"
EOF


%files
%dir %{OHPC_PUB}
%{install_path}
%{OHPC_MODULEDEPS}/%{compiler_family}/%{pname}
%doc README.md
%license LICENSE

%changelog
* Thu Dec 22 2022 Sol Jerome <solj@utdallas.edu> 1.0.0-3.ohpc
- Fix expected build to work without network
* Wed Dec 21 2022 Georgia Stuart <georgia.stuart@gmail.com> 1.0.0-2.ohpc
- Refactor out python dependencies to rely on python38-ohpc
- Fix path for Mamba executable
* Thu Dec 15 2022 Georgia Stuart <georgia.stuart@gmail.com> - 1.0.0
- Initial Mamba ohpc RPM
