#
# Conditional build:
%bcond_without	src		# build devel package with sources
%bcond_without	tests	# build without tests

%define		pkgname		blackfriday
Summary:	Markdown processor implemented in Go
Name:		golang-github-russross-%{pkgname}
Version:	1.4
Release:	1
License:	BSD
Group:		Libraries
Source0:	https://github.com/russross/blackfriday/archive/v%{version}/blackfriday-%{version}.tar.gz
# Source0-md5:	e66233912216753cc1b39875b81b74e2
URL:		https://github.com/russross/blackfriday
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_enable_debug_packages 0
%define		gopath		%{_libdir}/golang
%define		import_path	github.com/russross/%{pkgname}

%description
%{summary}.

%package devel
Summary:	%{summary}
Group:		Development/Languages
Requires:	golang(github.com/shurcooL/sanitized_anchor_name)
Provides:	golang(%{import_path}) = %{version}-%{release}
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description devel
%{summary}

This package contains library source intended for building other
packages which use import path with %{import_path} prefix.

%prep
%setup -q -n %{pkgname}-%{version}

%build
export GOPATH=$(pwd):%{gopath}

%if %{with test}
go test %{import_path}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with src}
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find -iname "*.go" '!' -iname "*_test.go") ; do
	install -d -p $RPM_BUILD_ROOT%{gopath}/src/%{import_path}/$(dirname $file)
	cp -pav $file $RPM_BUILD_ROOT%{gopath}/src/%{import_path}/$file
	echo "%{gopath}/src/%{import_path}/$file" >> devel.file-list
done
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with src}
%files devel -f devel.file-list
%defattr(644,root,root,755)
%doc README.md
%dir %{gopath}/src/github.com
%dir %{gopath}/src/github.com/russross
%dir %{gopath}/src/%{import_path}
%endif
