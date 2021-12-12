# TODO: use system tx: https://github.com/adobe-type-tools/afdko
#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Standalone CFF subroutinizer based on the AFDKO tx tool
Summary(pl.UTF-8):	Samodzielny generator podprocedur CFF oparty na narzędziu tx z AFDKO
Name:		python3-cffsubr
Version:	0.2.9.post1
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cffsubr/
Source0:	https://files.pythonhosted.org/packages/source/c/cffsubr/cffsubr-%{version}.tar.gz
# Source0-md5:	2e3de35a947539b76dd3e426f99373c4
URL:		https://github.com/adobe-type-tools/cffsubr
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_git_ls_files
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	python3-fonttools >= 4.10.2
%if "%{py3_ver}" == "3.6"
BuildRequires:	python3-importlib_resources
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.6
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Standalone CFF subroutinizer based on the AFDKO tx tool.

%description -l pl.UTF-8
Samodzielny generator podprocedur CFF oparty na narzędziu tx z pakietu
AFDKO.

%prep
%setup -q -n cffsubr-%{version}

%build
%py3_build

%if %{with tests}
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(echo $(pwd)/build-3/lib.*) \
%{__python3} -m pytest tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NOTICE README.md
%attr(755,root,root) %{_bindir}/cffsubr
%dir %{py3_sitedir}/cffsubr
%{py3_sitedir}/cffsubr/*.py
%{py3_sitedir}/cffsubr/__pycache__
%attr(755,root,root) %{py3_sitedir}/cffsubr/tx
%{py3_sitedir}/cffsubr-%{version}-py*.egg-info
