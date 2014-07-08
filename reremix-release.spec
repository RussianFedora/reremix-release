%define debug_package %{nil}
%define product_family RERemix Linux
%define variant_titlecase Server
%define variant_lowercase server
%define release_name Broken
%define base_release_version 7
%define full_release_version 7
%define dist_release_version 7
#define beta Beta
%define dist .el%{dist_release_version}.R

Name:           reremix-release
Version:        %{base_release_version}
Release:        1%{?dist}
Epoch:		1
Summary:        %{product_family} release file
Group:          System Environment/Base
License:        GPLv2
Provides:       reremix-release = %{epoch}:%{version}-%{release}
Provides:       centos-release = %{epoch}:%{version}-%{release}
Provides:       redhat-release = %{epoch}:%{version}-%{release}
Provides:       redhat-release = 7.0
Provides:       system-release = %{epoch}:%{version}-%{release}
Provides:       system-release = 7.0
Provides:       system-release(releasever) = %{base_release_version}
Obsoletes:	centos-release
Obsoletes:	sl-release
Source0:        reremix-release-%{base_release_version}.tar.xz
Source1:        85-display-manager.preset
Source2:        90-default.preset


%description
%{product_family} release files

%prep
%setup -q -n reremix-release-%{base_release_version}

%build
echo OK

%install
rm -rf %{buildroot}

# create /etc
mkdir -p %{buildroot}/etc

# create /etc/system-release and /etc/redhat-release
echo "%{product_family} release %{full_release_version} (%{release_name})" > %{buildroot}/etc/reremix-release
ln -s reremix-release %{buildroot}/etc/centos-release
ln -s reremix-release %{buildroot}/etc/system-release
ln -s reremix-release %{buildroot}/etc/redhat-release

# create /etc/os-release
cat << EOF >>%{buildroot}/etc/os-release
NAME="%{product_family}"
VERSION="%{full_release_version} (%{release_name})"
ID="reremix"
ID_LIKE="centos"
ID_LIKE="rhel"
ID_LIKE="fedora"
VERSION_ID="%{full_release_version}"
PRETTY_NAME="%{product_family} %{full_release_version} (%{release_name})"
ANSI_COLOR="0;31"
CPE_NAME="cpe:/o:centos:centos:7"
HOME_URL="https://www.russianfedora.pro/"
BUG_REPORT_URL="https://redmine.russianfedora.pro/"

EOF
# write cpe to /etc/system/release-cpe
echo "cpe:/o:centos:centos:7" > %{buildroot}/etc/system-release-cpe

# create /etc/issue and /etc/issue.net
echo '\S' > %{buildroot}/etc/issue
echo 'Kernel \r on an \m' >> %{buildroot}/etc/issue
cp %{buildroot}/etc/issue %{buildroot}/etc/issue.net
echo >> %{buildroot}/etc/issue

# copy GPG keys
mkdir -p -m 755 %{buildroot}/etc/pki/rpm-gpg
for file in RPM-GPG-KEY* ; do
    install -m 644 $file %{buildroot}/etc/pki/rpm-gpg
done

# set up the dist tag macros
install -d -m 755 %{buildroot}/etc/rpm
cat >> %{buildroot}/etc/rpm/macros.dist << EOF
# dist macros.

%%reremix_ver %{base_release_version}
%%centos_ver %{base_release_version}
%%rhel %{base_release_version}
%%dist %dist
%%el%{base_release_version} 1
EOF

# use unbranded datadir
mkdir -p -m 755 %{buildroot}/%{_datadir}/redhat-release
ln -s redhat-release %{buildroot}/%{_datadir}/reremix-release
ln -s redhat-release %{buildroot}/%{_datadir}/centos-release
install -m 644 EULA %{buildroot}/%{_datadir}/redhat-release

# use unbranded docdir
mkdir -p -m 755 %{buildroot}/%{_docdir}/redhat-release
ln -s redhat-release %{buildroot}/%{_docdir}/reremix-release
ln -s redhat-release %{buildroot}/%{_docdir}/centos-release
install -m 644 GPL %{buildroot}/%{_docdir}/redhat-release

# copy systemd presets
mkdir -p %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE1} %{buildroot}%{_prefix}/lib/systemd/system-preset/
install -m 0644 %{SOURCE2} %{buildroot}%{_prefix}/lib/systemd/system-preset/


%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
/etc/reremix-release
/etc/redhat-release
/etc/system-release
/etc/centos-release
%config(noreplace) /etc/os-release
%config /etc/system-release-cpe
%config(noreplace) /etc/issue
%config(noreplace) /etc/issue.net
/etc/pki/rpm-gpg/
/etc/rpm/macros.dist
%{_docdir}/redhat-release/*
%{_docdir}/reremix-release
%{_docdir}/centos-release
%{_datadir}/redhat-release/*
%{_datadir}/reremix-release
%{_datadir}/centos-release
%{_prefix}/lib/systemd/system-preset/*

%changelog
* Tue Jul  8 2014 Arkady L. Shane <ashejn@russianfedora.ru> - 7.0.el7.0.140617.3
- Yes. We planning RERemix 7
