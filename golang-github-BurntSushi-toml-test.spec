%if 0%{?fedora}
%global with_devel 0
%global with_bundled 0
%global with_debug 1
%global with_check 1
%else
%global with_devel 0
%global with_bundled 1
%global with_debug 0
%global with_check 0
%endif

%if 0%{?with_debug}
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

%global provider        github
%global provider_tld    com
%global project         BurntSushi
%global repo            toml-test
%global import_path     %{provider}.%{provider_tld}/%{project}/%{repo}
%global commit          85f50d0991feaca39fd7c3ad1047acbf9df90859
%global shortcommit     %(c=%{commit}; echo ${c:0:7})


Name:           golang-%{provider}-%{project}-%{repo}
Version:        0.2.0
Release:        0.14.git%{shortcommit}%{?dist}
Summary:        Language agnostic test suite for TOML
License:        WTFPL
URL:            https://%{import_path}
Source0:        https://%{import_path}/archive/%{commit}/%{repo}-%{commit}.tar.gz
ExclusiveArch:  %{go_arches}
Provides:       toml-test = %{version}-%{release}
BuildRequires:  golang >= 1.2.1-3

%description
toml-test is a higher-order program that tests other TOML decoders or
encoders. Tests are divided into two groups: invalid TOML data and valid TOML
data. Decoders that reject invalid TOML data pass invalid TOML tests. Decoders
that accept valid TOML data and output precisely what is expected pass valid
tests.



%if 0%{?with_devel}
%package devel
Summary:        Language agnostic test suite for TOML devel package
BuildArch:      noarch

%description devel
toml-test is a higher-order program that tests other TOML decoders or
encoders. Tests are divided into two groups: invalid TOML data and valid TOML
data. Decoders that reject invalid TOML data pass invalid TOML tests. Decoders
that accept valid TOML data and output precisely what is expected pass valid
tests.

Devel package.
%endif


%prep
%setup -q -n %{repo}-%{commit}


%build
mkdir -p _build/src/github.com/BurntSushi
ln -sf $(pwd) _build/src/github.com/BurntSushi/toml-test
export GOPATH=$(pwd)/_build:%{gopath}
mkdir bin

%if 0%{?with_debug}
function gobuild { go build -a -ldflags "-B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \n')" -v -x "$@"; }
%else
function gobuild { go build -a "$@"; }
%endif

gobuild -o bin/%{repo} %{import_path}


%install
install -D -p -m 0755 bin/%{repo} %{buildroot}%{_bindir}/%{repo}
mkdir -p  %{buildroot}%{_datadir}/%{repo}/
cp -a tests %{buildroot}%{_datadir}/%{repo}/

%if 0%{?with_devel}
# install devel source codes
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
%endif


%check
# no _test.go files so far


%files
%if 0%{?fedora}
%license COPYING
%else
%doc COPYING
%endif
%doc README.md
%{_bindir}/%{repo}
%{_datadir}/%{repo}/

%if 0%{?with_devel}
%files devel
%if 0%{?fedora}
%license COPYING
%else
%doc README.md COPYING
%endif
%doc README.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%{gopath}/src/%{import_path}
%endif


%changelog
* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.14.git85f50d0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.13.git85f50d0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Aug 02 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.12.git85f50d0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.11.git85f50d0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.10.git85f50d0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jul 21 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-0.9.git85f50d0
- https://fedoraproject.org/wiki/Changes/golang1.7

* Mon Feb 22 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.2.0-0.8.git85f50d0
- https://fedoraproject.org/wiki/Changes/golang1.6

* Wed Feb 03 2016 Fedora Release Engineering <releng@fedoraproject.org> - 0.2.0-0.7.git85f50d0
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jul 24 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-0.6.git85f50d0
- %%files in main subpackage if-else license
- Correct %%files if devel package
- Remove duplicated BR in devel package

* Wed Jul 15 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-0.5.git85f50d0
- Disable devel package
- Specify minimal version needed for golang

* Sun Jul 12 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-0.4.git85f50d0
- Remove unecessary Requires to golang

* Sun Jul 12 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-0.3.git85f50d0
- Update SPEC to take into account flags from SPEC generated with gofed

* Sun Jul 12 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-0.2.git85f50d0
- Only add sources once in %%files in devel package
- Correct dist tag
- devel package requires standard package
- Use %%{go_arches} for ExclusiveArch

* Fri Jul 3 2015 Julien Enselme <jujens@jujens.eu> - 0.2.0-0.1.git85f50d0
- Initial packaging
