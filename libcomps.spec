#
# TODO
# - fix missing -lm
# - convince upstream to fix SONAME: libcomps.so.0.1.6
#
# Conditional build:
%bcond_without	doc		# don't build doc
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

Summary:	Comps XML file manipulation library
Name:		libcomps
Version:	0.1.6
Release:	1
License:	GPL v2+
Group:		Development/Libraries
Source0:	https://github.com/midnightercz/libcomps/archive/%{name}-%{version}.tar.gz
# Source0-md5:	50611b9564f15b6a06e0f40f7683a0f0
URL:		https://github.com/midnightercz/libcomps/
BuildRequires:	check-devel
BuildRequires:	cmake
%{?with_doc:BuildRequires:	doxygen}
BuildRequires:	expat-devel
BuildRequires:	libxml2-devel
%{?with_doc:BuildRequires:	python-Sphinx}
%{?with_python2:BuildRequires:	python-devel}
%{?with_python3:BuildRequires:	python3-devel}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# Unresolved symbols: log10
%define		skip_post_check_so	libcomps.so.%{version}

%description
Libcomps is library for structure-like manipulation with content of
comps XML files. Supports read/write XML file, structure(s)
modification.

%package devel
Summary:	Development files for libcomps library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Development files for libcomps library

%package -n python-libcomps
Summary:	Python2 bindings for libcomps library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python-libcomps
Python2 bindings for libcomps library

%package -n python3-libcomps
Summary:	Python3 bindings for libcomps library
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description -n python3-libcomps
Python3 bindings for libcomps library

%prep
%setup -qn %{name}-%{name}-%{version}

%if %{with python3}
rm -rf py3
set -- *
install -d py3
cp -a "$@" py3
%endif

%build
%cmake \
	-DPYTHON_DESIRED:STRING=2 \
	libcomps/

%{__make}
%{__make} docs
%{__make} pydocs

%if %{with python3}
cd py3
%cmake \
	-DPYTHON_DESIRED:STRING=3 \
	libcomps/
%{__make}
cd -
%endif

%if %{with tests}
%{__make} test
%if %{with python3}
cd py3
%{__make} pytest
cd -
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%if %{with python3}
cd py3
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%py3_ocomp $RPM_BUILD_ROOT%{py3_sitedir}
%py3_comp $RPM_BUILD_ROOT%{py3_sitedir}
cd -
%endif

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
%doc docs/libcomps-doc/html
%doc src/python/docs/html
%{_libdir}/libcomps.so
%{_includedir}/libcomps

%files -n python-libcomps
%defattr(644,root,root,755)
%dir %{py_sitedir}/libcomps
%{py_sitedir}/libcomps/__init__.py[co]
%attr(755,root,root) %{py_sitedir}/libcomps/_libpycomps.so

%if %{with python3}
%files -n python3-libcomps
%defattr(644,root,root,755)
%dir %{py3_sitedir}/libcomps
%{py3_sitedir}/libcomps/__init__.py
%attr(755,root,root) %{py3_sitedir}/libcomps/_libpycomps.so
%{py3_sitedir}/libcomps/__pycache__
%endif
