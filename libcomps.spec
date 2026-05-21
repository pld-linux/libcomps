#
# Conditional build:
%bcond_without	doc	# (doxygen and sphinx) documentation

Summary:	Comps XML file manipulation library
Summary(pl.UTF-8):	Biblioteka operacji na plikach Comps XML
Name:		libcomps
Version:	0.1.24
Release:	1
License:	GPL v2+
Group:		Libraries
#Source0Download: https://github.com/rpm-software-management/libcomps/releases
Source0:	https://github.com/rpm-software-management/libcomps/archive/%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	8d07648e6226cd1788381b4a36430935
Patch0:		%{name}-build.patch
URL:		https://github.com/rpm-software-management/libcomps
BuildRequires:	check-devel
BuildRequires:	cmake >= 3.10
%{?with_doc:BuildRequires:	doxygen}
BuildRequires:	expat-devel >= 1.95
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	python3-setuptools
BuildRequires:	rpmbuild(macros) >= 2.047
%{?with_doc:BuildRequires:	sphinx-pdg}
BuildRequires:	rpm-pythonprov
BuildRequires:	zlib-devel
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
%patch -P 0 -p1

%build
install -d build
cd build
%cmake ../libcomps \
	-DENABLE_DOCS:BOOL=%{__ON_OFF doc} \
	-DENABLE_TESTS:BOOL=OFF

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
%{_libdir}/libcomps.so.0

%files devel
%defattr(644,root,root,755)
%{_libdir}/libcomps.so
%{_includedir}/libcomps
%{_pkgconfigdir}/libcomps.pc

%files -n python3-libcomps
%defattr(644,root,root,755)
%if %{with doc}
%doc build/src/python/docs/html/{*.html,*.js,_static}
%endif
%dir %{py3_sitedir}/libcomps
%{py3_sitedir}/libcomps/__init__.py
%{py3_sitedir}/libcomps/_libpycomps.so
%{py3_sitedir}/libcomps/__pycache__
%{py3_sitedir}/libcomps-*-py*.egg-info
