# Copyright (c) 2021 ABLECLOUD Co. Ltd
# 이 파일은 rpmbuild를 이용하여 ablestack-wall을 빌드하기 위한 내용을 정의한 spec파일입니다. 
# 최초 작성일 : 2021. 08. 26

%define _topdir %(echo $PWD)/rpmbuild

Name: ablestack-wall
Version: %{?version}%{!?version:1.0}
Release: %{?release}%{!?release:1.wip.el8.noarch}
Source0: %{name}-%{version}.tar.gz
Summary: ablestack-wall package

Group: ABLECLOUD
License: None
URL: https://github.com/ablecloud-team/ablestack-monitor.git
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: /bin/bash, /bin/mkdir, /bin/cp
Requires: /bin/bash, /bin/mkdir, /bin/cp

%description
ablestack-wall package

%define debug_package %{nil}
%define _unpackaged_files_terminate_build 0
%define _missing_doc_files_terminate_build 0

%prep
%setup -q

%build

#configure
#make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/usr/share/ablestack/ablestack-wall
cp -r /root/ablestack-monitor $RPM_BUILD_ROOT/usr/share/ablestack/ablestack-wall


%post
#echo 'ABLESTACK-Wall script'
/usr/share/ablestack/ablestack-wall/tools/make-rpm/ablestack-wall.sh&
#echo 'ABLESTACK-Wall complete!'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
#%doc

%attr(0755,root,root)/usr/share/ablestack/ablestack-wall/*

%changelog
* Thu Apr 1 2021 ABLESTACK <ablecloud@ablecloud.io> - 0.1
-Initial RPM