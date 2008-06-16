Summary:	Network monitoring tools for tracking IP addresses on the network
Name:		arpwatch
Version:	2.1a15
Release:	%mkrel 3
Epoch:		2
License:	BSD
Group:		Monitoring
URL:		ftp://ftp.ee.lbl.gov
Source0:	ftp://ftp.ee.lbl.gov/arpwatch-%{version}.tar.gz
Source1:	arpwatch.init
Source2:	arpwatch.sysconfig
Patch0:		arpwatch-Makefile-fixes.patch
Patch1:		arpwatch-2.1a11-noip.diff
Patch2:		arpwatch-2.1a13-drop_root.diff
Patch3:		arpwatch-drop-man.patch
Patch4:		arpwatch-2.1a13-mail_user.diff
BuildRequires:	libpcap-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	sendmail-command
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
The arpwatch package contains arpwatch and arpsnmp.  Arpwatch and arpsnmp
are both network monitoring tools.  Both utilities monitor Ethernet or
FDDI network traffic and build databases of Ethernet/IP address pairs,
and can report certain changes via email.

Install the arpwatch package if you need networking monitoring devices
which will automatically keep traffic of the IP addresses on your
network.

%prep

%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p0 -b .droproot
%patch3 -p0 -b .droprootman
%patch4 -p1 -b .mailuser

cp %{SOURCE1} arpwatch.init
cp %{SOURCE2} arpwatch.sysconfig

%build
libtoolize --copy --force

%serverbuild

%configure

%make \
    ARPDIR=%{_localstatedir}/lib/arpwatch \
    SENDMAIL="%{_sbindir}/sendmail"

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_localstatedir}/lib/arpwatch
install -d %{buildroot}%{_mandir}/man8

%makeinstall_std install-man

for n in arp2ethers massagevendor; do
    install -m755 $n %{buildroot}%{_localstatedir}/lib/arpwatch
done

for n in *.awk *.dat; do
    install -m644 $n %{buildroot}%{_localstatedir}/lib/arpwatch
done

install -m0755 arpwatch.init %{buildroot}%{_initrddir}/arpwatch
install -m0644 arpwatch.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/arpwatch 

%pre
%_pre_useradd arpwatch %{_localstatedir}/lib/arpwatch /bin/sh

%post
%_post_service arpwatch

%preun
%_preun_service arpwatch

%postun
%_postun_userdel arpwatch

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README CHANGES
%attr(0755,root,root) %{_initrddir}/arpwatch
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/arpwatch
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
%{_localstatedir}/lib/arpwatch/massagevendor


