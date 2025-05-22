# TODO: use system tx: https://github.com/adobe-type-tools/afdko
#
# Conditional build:
%bcond_without	tests	# unit tests

Summary:	Standalone CFF subroutinizer based on the AFDKO tx tool
Summary(pl.UTF-8):	Samodzielny generator podprocedur CFF oparty na narzędziu tx z AFDKO
Name:		python3-cffsubr
Version:	0.3.0
Release:	1
License:	Apache v2.0
Group:		Libraries/Python
#Source0Download: https://pypi.org/simple/cffsubr/
Source0:	https://files.pythonhosted.org/packages/source/c/cffsubr/cffsubr-%{version}.tar.gz
# Source0-md5:	9ea6396f228e278ff7660dc4edde4c37
URL:		https://github.com/adobe-type-tools/cffsubr
BuildRequires:	python3-devel >= 1:3.9
BuildRequires:	python3-setuptools
BuildRequires:	python3-setuptools_git_ls_files
BuildRequires:	python3-setuptools_scm
%if %{with tests}
BuildRequires:	adobe-afdko
BuildRequires:	python3-fonttools >= 4.10.2
BuildRequires:	python3-pytest
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
Requires:	python3-modules >= 1:3.9
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Standalone CFF subroutinizer based on the AFDKO tx tool.

%description -l pl.UTF-8
Samodzielny generator podprocedur CFF oparty na narzędziu tx z pakietu
AFDKO.

%prep
%setup -q -n cffsubr-%{version}

# Do not build the extension, which is a copy of the “tx” executable from
# adobe-afdko. Patch out the custom build backend, which would have generated
# dependencies needed for building the extension.
sed -r -i 's/(ext_modules=)/# \1/' setup.py
sed -r -i 's/^(build-backend|backend-path)/# \1/' pyproject.toml

# Remove bundled adobe-afdko:
rm -rf external

%build
%py3_build_pyproject

%if %{with tests}
%{__python3} -m zipfile -e build-3/*.whl build-3-test
ln -s %{_bindir}/tx build-3-test/cffsubr/tx
# use explicit plugins list for reliable builds (delete PYTEST_PLUGINS if empty)
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTEST_PLUGINS= \
%{__python3} -m pytest -o pythonpath="$PWD/build-3-test" tests
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc NOTICE README.md
%attr(755,root,root) %{_bindir}/cffsubr
%dir %{py3_sitescriptdir}/cffsubr
%{py3_sitescriptdir}/cffsubr/*.py
%{py3_sitescriptdir}/cffsubr/__pycache__
%{py3_sitescriptdir}/cffsubr-%{version}.dist-info
