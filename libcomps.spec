#
# TODO
# - fix missing -lm
# - convince upstream to fix SONAME: libcomps.so.0.1.6
#
# Conditional build:
%bcond_without	doc	# don't build (doxygen and sphinx) docs

Summary:	Comps XML file manipulation library
Summary(pl.UTF-8):	Biblioteka operacji na plikach Comps XML
Name:		libcomps
Version:	0.1.20
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/libcomps/releases
Source0:	https://github.com/rpm-software-management/libcomps/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	478b2e8d4189eee9480805a76549a795
Patch0:		%{name}-build.patch
URL:		https://github.com/rpm-software-management/libcomps
BuildRequires:	check-devel
BuildRequires:	cmake >= 2.6
%{?with_doc:BuildRequires:	doxygen}
BuildRequires:	expat-devel >= 1.95
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	rpmbuild(macros) >= 1.742
%{?with_doc:BuildRequires:	sphinx-pdg}
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
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake ../libcomps \
	%{cmake_on_off doc ENABLE_DOCS} \
	-DENABLE_TESTS:BOOL=NO

%{__make}
%{?with_doc:%{__make} pydocs}
%if %{with tests}
%{__make} test
%endif


%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}

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
%attr(755,root,root) %{_libdir}/libcomps.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libcomps.so
%{_includedir}/libcomps
%{_pkgconfigdir}/libcomps.pc

%files -n python3-libcomps
%{?with_doc:%doc build/src/python/docs/html/{*.html,*.js,_static}}
%defattr(644,root,root,755)
%dir %{py3_sitedir}/libcomps
%{py3_sitedir}/libcomps/__init__.py
%attr(755,root,root) %{py3_sitedir}/libcomps/_libpycomps.so
%{py3_sitedir}/libcomps/__pycache__
%{py3_sitedir}/libcomps-*-py*.egg-info
