Summary:	Network monitoring tools for tracking IP addresses on the network
Name:		arpwatch
Version:	2.1a15
Release:	%mkrel 10
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
Patch5:		arpwatch-2.1a15-LDFLAGS.diff
BuildRequires:	libpcap-devel
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires:	sendmail-command
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
%patch5 -p0

cp %{SOURCE1} arpwatch.init
cp %{SOURCE2} arpwatch.sysconfig

%build
libtoolize --copy --force

%serverbuild
%configure2_5x
%make \
    ARPDIR=%{_localstatedir}/lib/arpwatch \
    SENDMAIL="%{_sbindir}/sendmail" \
    LDFLAGS="%ldflags"

%install
rm -rf %{buildroot}

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
rm -rf %{buildroot}

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


%changelog
* Mon May 02 2011 Oden Eriksson <oeriksson@mandriva.com> 2:2.1a15-9mdv2011.0
+ Revision: 662790
- mass rebuild

* Mon Nov 29 2010 Oden Eriksson <oeriksson@mandriva.com> 2:2.1a15-8mdv2011.0
+ Revision: 603184
- rebuild

* Mon Feb 22 2010 Sandro Cazzaniga <kharec@mandriva.org> 2:2.1a15-7mdv2010.1
+ Revision: 509459
- Use %%configure2_5x instead of %%configure.

* Sun Aug 09 2009 Oden Eriksson <oeriksson@mandriva.com> 2:2.1a15-6mdv2010.0
+ Revision: 413037
- rebuild

* Sat Dec 20 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.1a15-5mdv2009.1
+ Revision: 316494
- use %%ldflags

* Wed Oct 29 2008 Oden Eriksson <oeriksson@mandriva.com> 2:2.1a15-4mdv2009.1
+ Revision: 298234
- rebuilt against libpcap-1.0.0

* Mon Jun 16 2008 Thierry Vignaud <tv@mandriva.org> 2:2.1a15-3mdv2009.0
+ Revision: 220356
- rebuild

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Fri Jan 11 2008 Thierry Vignaud <tv@mandriva.org> 2:2.1a15-2mdv2008.1
+ Revision: 148466
- rebuild
- kill re-definition of %%buildroot on Pixel's request

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot


* Wed Mar 07 2007 Oden Eriksson <oeriksson@mandriva.com> 2.1a15-1mdv2007.0
+ Revision: 134277
- 2.1a15
- bunzip patches and sources

* Fri Dec 22 2006 Oden Eriksson <oeriksson@mandriva.com> 2:2.1a13-6mdv2007.1
+ Revision: 101574
- Import arpwatch

* Tue May 16 2006 Pablo Saratxaga <pablo@mandriva.com> 2.1a13-6mdk
- changed init script to use generic (translator-friendly) strings

* Fri Oct 07 2005 Oden Eriksson <oeriksson@mandriva.com> 2.1a13-5mdk
- added P2,P3,P4 from fedora, rediffed P2 and P4
- fix deps

* Fri Aug 12 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.1a13-4mdk
- fix rpmlint errors (PreReq)

* Thu Aug 11 2005 Nicolas Lécureuil <neoclust@mandriva.org> 2.1a13-3mdk
- fix rpmlint errors (PreReq)

* Thu Jul 14 2005 Oden Eriksson <oeriksson@mandriva.com> 2.1a13-2mdk
- rebuilt against new libpcap-0.9.1 (aka. a "play safe" rebuild)

* Sat Nov 20 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.1a13-1mdk
- 2.1a13
- fixed S1 to make it configurable using S2

* Wed Jun 02 2004 Oden Eriksson <oeriksson@mandrakesoft.com> 2.1a11-5mdk
- added P1
- misc spec file fixes

* Tue Apr 20 2004 Michael Scherer <misc@mandrake.org> 2.1a11-4mdk
- remove csh requirement

