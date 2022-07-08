Summary:	Network monitoring tools for tracking IP addresses on the network
Name:		arpwatch
Version:	3.3
Release:	1
License:	BSD
Group:		Monitoring
Url:		ftp://ftp.ee.lbl.gov
Source0:	https://ee.lbl.gov/downloads/arpwatch/%{name}-%{version}.tar.gz
Source1:	https://src.fedoraproject.org/rpms/arpwatch/raw/master/f/arpwatch.service
Source2:	arpwatch.sysconfig
Source3:	https://github.com/archlinux/svntogit-community/raw/packages/arpwatch/trunk/ethercodes.dat.gz
Patch0:		arpwatch-Makefile-fixes.patch
Patch2:		arpwatch-2.1a13-drop_root.diff
Patch3:		arpwatch-drop-man.patch
Patch5:		arpwatch-2.1a15-LDFLAGS.diff

BuildRequires:	pkgconfig(libpcap)
# Just so autoconf can locate the sendmail binary
BuildRequires:	postfix
Requires(post,preun,pre,postun):	rpm-helper
Requires:	sendmail-command

%description
The arpwatch package contains arpwatch and arpsnmp.  Arpwatch and arpsnmp
are both network monitoring tools.  Both utilities monitor Ethernet or
FDDI network traffic and build databases of Ethernet/IP address pairs,
and can report certain changes via email.

Install the arpwatch package if you need networking monitoring devices
which will automatically keep traffic of the IP addresses on your
network.

%prep
%autosetup -p1

cp %{SOURCE1} arpwatch.init
cp %{SOURCE2} arpwatch.sysconfig

%build
libtoolize --copy --force

%serverbuild
%configure
%make_build \
	ARPDIR=%{_localstatedir}/lib/arpwatch \
	SENDMAIL="%{_sbindir}/sendmail" \
	LDFLAGS="%ldflags"

%install
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_prefix}%{_sysconfdir}/rc.d
install -d %{buildroot}/lib/systemd/system
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_localstatedir}/lib/arpwatch
install -d %{buildroot}%{_mandir}/man8

%make_install

for n in arp2ethers; do
    install -m755 $n %{buildroot}%{_localstatedir}/lib/arpwatch
done

for n in *.awk *.dat; do
    install -m644 $n %{buildroot}%{_localstatedir}/lib/arpwatch
done

rm -rf %{buildroot}%{_prefix}%{_sysconfdir}/rc.d
install -m0755 %{S:1} %{buildroot}/lib/systemd/system
install -m0644 %{S:2} %{buildroot}%{_sysconfdir}/sysconfig/arpwatch

cp %{S:3} .
gunzip ethercodes.dat.gz
cp ethercodes.dat %{buildroot}%{_localstatedir}/lib/arpwatch/

%pre
%_pre_useradd arpwatch %{_localstatedir}/lib/arpwatch /bin/sh

%post
%_post_service arpwatch

%preun
%_preun_service arpwatch

%postun
%_postun_userdel arpwatch

%files
%doc README CHANGES
/lib/systemd/system/arpwatch.service
%config(noreplace) %{_sysconfdir}/sysconfig/arpwatch
%{_sbindir}/*
%{_mandir}/man*/*
%dir %attr(0755,arpwatch,arpwatch) %{_localstatedir}/lib/arpwatch
%config(noreplace) %{_localstatedir}/lib/arpwatch/arp.dat
#
# (fg) 20010403 DON'T PUT THIS AS NOREPLACE! Ethernet codes are bound to
# change, and if ever you have a new one, submit it to arpwatch author!
#
%config %{_localstatedir}/lib/arpwatch/ethercodes.dat
%{_localstatedir}/lib/arpwatch/*.awk
%{_localstatedir}/lib/arpwatch/arp2ethers
