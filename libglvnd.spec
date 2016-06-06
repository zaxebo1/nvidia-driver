%global commit0 8277115b22757c288d990574065c433e4505015a
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Name:           libglvnd
Version:        0.1.0
Release:        3.%{?shortcommit0}%{?dist}
Summary:        The GL Vendor-Neutral Dispatch library

License:        MIT
URL:            https://github.com/NVIDIA/%{name}
Source0:        https://github.com/NVIDIA/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:        https://raw.githubusercontent.com/aritger/linux-opengl-abi-proposal/master/linux-opengl-abi-proposal.txt

%if 0%{?rhel} == 6
BuildRequires:  autoconf268
%else
BuildRequires:  autoconf
%endif

BuildRequires:  automake
BuildRequires:  pkgconfig(xorg-server) >= 1.11.0
BuildRequires:  pkgconfig(x11)
BuildRequires:  pkgconfig(xv)
BuildRequires:  python

Requires:       xorg-x11-server-Xorg

Provides:       %{name}-server-module = %{version}-%{release}
Obsoletes:      %{name}-server-module < %{version}-%{release}

%description
This is a work-in-progress implementation of the vendor-neutral dispatch layer
for arbitrating OpenGL API calls between multiple vendors on a per-screen basis.

Currently, only the GLX window-system API and OpenGL are supported, but in the
future this library may support EGL and OpenGL ES as well.

%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.

%prep
%setup -qn %{name}-%{commit0}
cp %{SOURCE1} .

%build
%if 0%{?rhel} == 6
autoreconf268 -vif
%else
autoreconf -vif
%endif

%configure \
    --disable-static \
    --enable-asm \
    --enable-tls

make %{?_smp_mflags}

%install
%make_install

find %{buildroot} -name '*.la' -delete

# Do not use libGL gvnd as per default Nvidia installation (only 361.xx)
#rm -f %{buildroot}%{_libdir}/libGL.so*

# Move libraries
mkdir -p %{buildroot}%{_sysconfdir}/ld.so.conf.d/
echo "%{_libdir}/%{name}" > %{buildroot}%{_sysconfdir}/ld.so.conf.d/%{name}-%{_lib}.conf
mkdir %{buildroot}%{_libdir}/%{name}
mv %{buildroot}%{_libdir}/*.* %{buildroot}%{_libdir}/%{name}/

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%dir %{_libdir}/%{name}
%{_libdir}/%{name}/libGL.so.*
%{_libdir}/%{name}/libGLdispatch.so.*
%{_libdir}/%{name}/libGLESv1_CM.so.*
%{_libdir}/%{name}/libGLESv2.so.*
%{_libdir}/%{name}/libGLX.so.*
%{_libdir}/%{name}/libOpenGL.so.*
%{_sysconfdir}/ld.so.conf.d/%{name}-%{_lib}.conf

%files devel
%doc README.md
%doc linux-opengl-abi-proposal.txt
%{_includedir}/*
%{_libdir}/%{name}/libGL.so
%{_libdir}/%{name}/libGLdispatch.so
%{_libdir}/%{name}/libGLESv1_CM.so
%{_libdir}/%{name}/libGLESv2.so
%{_libdir}/%{name}/libGLX.so
%{_libdir}/%{name}/libOpenGL.so
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Mon May 02 2016 Simone Caronni <negativo17@gmail.com> - 0.1.0-3.8277115
- Update sources.

* Fri Apr 08 2016 Simone Caronni <negativo17@gmail.com> - 0.1.0-2.5a69af6
- Fix package release version.

* Fri Apr 08 2016 Simone Caronni <negativo17@gmail.com> - 0.1.0-1
- Update to version 0.1.0, minimum version required for Nvidia drivers 364.15+.

* Thu Mar 31 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-20.c5bcda3
- Update to latest snapshot.
- Fix build on RHEL 6.

* Wed Mar 30 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-19.3402e11
- Update to latest snapshot.
- Obsolete libglvnd-server-module, now uses recently merged GLX_EXT_libglvnd
  extension.

* Tue Mar 22 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-18.af2aeb0
- Update to latest sources.

* Sun Feb 28 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-17.cd9c312
- Update to latest sources, switch back to glvnd libGL.
- X.org module is loaded by the driver; drop config file:
  https://github.com/NVIDIA/libglvnd/pull/66

* Fri Feb 26 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-16.dc267e2
- Update to latest sources.

* Tue Feb 16 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-15.4d977ea
- Update to latest sources.
- Do not use libGL as in default Nvidia setup, otherwise environment variable
  __GLVND_DISALLOW_PATCHING=1 is required.

* Tue Feb 09 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-14.2367100
- Update to latest sources.
- Install everything on any distribution.

* Sun Jan 31 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-13.82e0d23
- Enable additional options.

* Tue Jan 26 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-12.82e0d23
- Make all components conditional on distribution.
- Update to latest snapshot.

* Sat Jan 23 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-11.ba0b05a
- Update to latest commits.

* Thu Jan 21 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-10.ca8e52b
- Remove ELF filtering parameter on configure (thanks Marcin Kurek).

* Thu Jan 14 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-9.ca8e52b
- Update to latest snapshot.
- Add headers to devel subpackage.

* Mon Jan 11 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-8.e5225e3
- Update to latest snapshot.

* Tue Jan 05 2016 Simone Caronni <negativo17@gmail.com> - 0.0.0-7.362c359
- Update to latest snapshot.
- Build all components and override base system libraries.

* Sun Dec 06 2015 Simone Caronni <negativo17@gmail.com> - 0.0.0-6.3194739
- Update to latest sources.

* Wed Nov 18 2015 Simone Caronni <negativo17@gmail.com> - 0.0.0-5
- Update to latest commits.

* Tue Oct 13 2015 Simone Caronni <negativo17@gmail.com> - 0.0.0-4
- Update to latest sources.

* Wed Sep 02 2015 Simone Caronni <negativo17@gmail.com> - 0.0.0-3
- Update to latest commits.

* Wed Aug 12 2015 Simone Caronni <negativo17@gmail.com> - 0.0.0-2
- Update to latest commits.
- Disable all extra components unless explicitly requested.

* Tue Aug 04 2015 Simone Caronni <negativo17@gmail.com> - 0.0.0-1
- First build.
