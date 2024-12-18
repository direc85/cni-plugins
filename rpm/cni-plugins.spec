#
# spec file for package cni-plugins
#
# Copyright (c) 2024 SUSE LLC
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via https://bugs.opensuse.org/
#


%define         cni_bin_dir  %{_libexecdir}/cni
%define         cni_doc_dir  %{_docdir}/cni-plugins
Name:           cni-plugins
Version:        1.6.1
Release:        1
Summary:        Container Network Interface plugins
License:        Apache-2.0
Group:          System/Management
URL:            https://github.com/containernetworking/plugins
Source:         %{name}-%{version}.tar.xz
BuildRequires:  shadow-utils
BuildRequires:  pkgconfig(systemd)
BuildRequires:  xz
#BuildRequires:  golang(API) >= 1.21
BuildRequires:  golang(API) >= 1.23
Requires:       cni
#Requires(post): %%fillup_prereq
%{?systemd_requires}

%description
The CNI (Container Network Interface) project consists of a
specification and libraries for writing plugins to configure
network interfaces in Linux containers, along with a number of
supported plugins. CNI concerns itself only with network
connectivity of containers and removing allocated resources when
the container is deleted. Because of this focus, CNI has a wide
range of support and the specification is simple to implement.

These are the additional CNI network plugins provided by
the containernetworking team.

%prep
%autosetup -n %{name}-%{version}/plugins

%build
%ifnarch ppc64
export GOFLAGS="-buildmode=pie"
%endif

export GOTMPDIR=${TMPDIR:-$(realpath .)}/.tmp-go
mkdir -p $GOTMPDIR

export GOCACHE=${TMPDIR:-$(realpath .)}/.tmp-gocache
mkdir -p $GOCACHE

export TMPDIR=${TMPDIR:-$(realpath .)}/.tmp
mkdir -p $TMPDIR

./build_linux.sh

%install

# install the plugins
install -m 755 -d "%{buildroot}%{cni_bin_dir}"
cp bin/* "%{buildroot}%{cni_bin_dir}/"

# documentation
install -m 755 -d "%{buildroot}%{cni_doc_dir}"

#%%post
#%%{fillup_only -n %%{name}}

%files
%dir %{cni_doc_dir}
%doc CONTRIBUTING.md
%doc README.md
%license LICENSE
%dir %{cni_bin_dir}
%{cni_bin_dir}/*
