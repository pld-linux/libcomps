#
# TODO
# - fix missing -lm
# - convince upstream to fix SONAME: libcomps.so.0.1.6
#
# Conditional build:
%bcond_without	doc	# don't build (doxygen and sphinx) docs
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Comps XML file manipulation library
Summary(pl.UTF-8):	Biblioteka operacji na plikach Comps XML
Name:		libcomps
Version:	0.1.6
Release:	6
License:	GPL v2+
Group:		Libraries
Source0:	https://github.com/midnightercz/libcomps/archive/%{name}-%{version}.tar.gz
# Source0-md5:	50611b9564f15b6a06e0f40f7683a0f0
Patch0:		%{name}-link.patch
Patch1:		python-install-dir.patch
URL:		https://github.com/midnightercz/libcomps/
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.6
%{?with_doc:BuildRequires:	doxygen}
BuildRequires:	expat-devel >= 1.95
BuildRequires:	libxml2-devel >= 2.0
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-modules
%{?with_doc:BuildRequires:	sphinx-pdg-2}
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-modules
%{?with_doc:BuildRequires:	sphinx-pdg}
%endif
BuildRequires:	rpm-pythonprov
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libcomps is library for structure-like manipulation with content of
comps XML files. Supports read/write XML file, structure(s)
modification.

%description -l pl.UTF-8
Libcomps to bibliotek do operacji strukturalnych na treści plików
comps XML. Obsługiwany jest odczyt i zapis pliku XML oraz modyfikacja
struktury.

%package devel
Summary:	Development files for libcomps library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki libcomps
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	expat-devel >= 1.95
Requires:	libxml2-devel >= 2.0

%description devel
Development files for libcomps library

%description devel -l pl.UTF-8
Pliki programistyczne biblioteki libcomps.

%package -n python-libcomps
Summary:	Python 2.x bindings for libcomps library
Summary(pl.UTF-8):	Wiązania Pythona 2.x do biblioteki libcomps
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python-libcomps
Python 2.x bindings for libcomps library.

%description -n python-libcomps -l pl.UTF-8
Wiązania Pythona 2.x do biblioteki libcomps.

%package -n python3-libcomps
Summary:	Python 3.x bindings for libcomps library
Summary(pl.UTF-8):	Wiązania Pythona 3.x do biblioteki libcomps
Group:		Libraries/Python
Requires:	%{name} = %{version}-%{release}

%description -n python3-libcomps
Python 3.x bindings for libcomps library.

%description -n python3-libcomps -l pl.UTF-8
Wiązania Pythona 3.x do biblioteki libcomps.

%prep
%setup -qn %{name}-%{name}-%{version}
%patch0 -p1
%patch1 -p1

%build
install -d build
cd build
%cmake ../libcomps \
	-DPYTHON_DESIRED:STRING=2 \
	-DPYTHON_INSTALL_DIR="%{py_sitedir}" \
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build-2 \
	-DCMAKE_CXX_COMPILER_WORKS=1 \
	-DCMAKE_CXX_COMPILER="%{__cc}"

%{__make}
%{__make} docs
%{__make} pydocs
cd ..

%if %{with python3}
install -d build-py3
cd build-py3
%cmake ../libcomps \
	-DPYTHON_DESIRED:STRING=3 \
	-DPYTHON_INSTALL_DIR="%{py3_sitedir}" \
	-DSPHINX_EXECUTABLE=/usr/bin/sphinx-build-3 \
	-DCMAKE_CXX_COMPILER_WORKS=1 \
	-DCMAKE_CXX_COMPILER="%{__cc}"

%{__make}
%{__make} pydocs
cd ..
%endif

%if %{with tests}
%{__make} -C build test
%if %{with python3}
%{__make} -C build-py3 pytest
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%if %{with python3}
%{__make} -C build-py3 install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
%endif

install -d $RPM_BUILD_ROOT%{_pkgconfigdir}
%{__sed} -e 's,^prefix=.*,prefix=%{_prefix},' \
	-e 's,@LIB_SUFFIX@,%{_lib},' \
	-e 's,@VERSION@,%{version},' \
	libcomps.pc.in > $RPM_BUILD_ROOT%{_pkgconfigdir}/libcomps.pc

/sbin/ldconfig -n $RPM_BUILD_ROOT%{_libdir}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc README.md COPYING
%attr(755,root,root) %{_libdir}/libcomps.so.0.1.6

%files devel
%defattr(644,root,root,755)
%doc build/docs/libcomps-doc/html/*
%attr(755,root,root) %{_libdir}/libcomps.so
%{_includedir}/libcomps
%{_pkgconfigdir}/libcomps.pc

%if %{with python2}
%files -n python-libcomps
%defattr(644,root,root,755)
%doc build/src/python/docs/html/{*.html,*.js,_images,_static}
%dir %{py_sitedir}/libcomps
%{py_sitedir}/libcomps/__init__.py[co]
%attr(755,root,root) %{py_sitedir}/libcomps/_libpycomps.so
%endif

%if %{with python3}
%files -n python3-libcomps
%doc build-py3/src/python/docs/html/{*.html,*.js,_images,_static}
%defattr(644,root,root,755)
%dir %{py3_sitedir}/libcomps
%{py3_sitedir}/libcomps/__init__.py
%attr(755,root,root) %{py3_sitedir}/libcomps/_libpycomps.so
%{py3_sitedir}/libcomps/__pycache__
%endif
