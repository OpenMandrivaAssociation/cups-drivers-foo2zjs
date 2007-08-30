%define rname foo2zjs
%define snap 20070820

Summary:	A linux printer driver for ZjStream protocol
Name:		cups-drivers-%{rname}
Version:	0.0
Release:	%mkrel 0.%{snap}.1
Group:		System/Printing
License:	GPL
URL:		http://foo2zjs.rkkda.com/
Source0:	http://foo2zjs.rkkda.com/foo2zjs.tar.gz
Patch0:		foo2zjs-system_icc2ps.diff
Patch1:		foo2zjs-install_fix.diff
Patch2:		foo2zjs-cflags.diff
Patch3:		foo2zjs-system_jbig.diff
BuildRequires:	lcms
BuildRequires:	ghostscript
BuildRequires:	foomatic-filters
BuildRequires:	jbig-devel
Requires:	lcms
Requires:	wget
Requires:	foomatic-db-engine
# psutils, unzip, and mscompress needed by the foo2zjs driver
Requires:	psutils, unzip
%if %mdkversion >= 200700
Requires:	mscompress
%endif
Conflicts:	cups-drivers = 2007
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007
Conflicts:	foomatic-db < 1:3.0.2-1.20070820.1mdv2008.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-root

%description
foo2zjs is an open source printer driver for printers that use the Zenographics
ZjStream wire protocol for their print data, such as the Minolta/QMS magicolor
2300 DL. These printers are often erroneously referred to as winprinters or GDI
printers.

foo2zjs: a linux printer driver for ZjStream protocol
e.g. Minolta magicolor 2200/2300/2430 DL, HP LaserJet 1018/1020/1022

This package provides foomatic and cups drivers for the following printers:

 o Generic OAKT Printer
 o Generic ZjStream Printer
 o HP Color LaserJet 1500
 o HP Color LaserJet 1600
 o HP Color LaserJet 2600n
 o HP LaserJet 1000
 o HP LaserJet 1005
 o HP LaserJet 1018
 o HP LaserJet 1020
 o HP LaserJet 1022
 o HP LaserJet M1005 MFP
 o KonicaMinolta magicolor 2480 MF
 o KonicaMinolta magicolor 2490 MF
 o KonicaMinolta magicolor 2530 DL
 o Minolta Color PageWorks/Pro L
 o Minolta magicolor 2200 DL
 o Minolta magicolor 2300 DL
 o Minolta magicolor 2430 DL
 o Samsung CLP-300
 o Samsung CLP-600
 o Samsung CLX-3160
 o Xerox Phaser 6110
 o Xerox Phaser 6115MFP

%prep

%setup -q -n %{rname}
%patch0 -p1
%patch1 -p0
%patch2 -p0
%patch3 -p0

# fix attribs
chmod 644 COPYING ChangeLog INSTALL INSTALL.usb README

%build
make CFLAGS="%{optflags}"

# Fit udev rules to stricter syntax of new udev
# (blino) don't try to rename the device,
#         it has already been renamed to the exact same name in 50-mdk.rules
#         so udev would skip the rule
perl -p -i -e 's:(KERNEL|BUS|SYSFS.*?)=([^=]):$1==$2:g;s{SYMLINK=}{SYMLINK+=}g;s{(?:NAME|MODE)=.*?,\s*}{}g' hplj10xx.rules

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/foomatic/db/source/{driver,opt,printer}
install -d %{buildroot}%{_datadir}/cups/model/%{rname}
install -d %{buildroot}%{_sysconfdir}/udev/rules.d

make install \
    PREFIX=%{buildroot}%{_prefix} \
    BIN=%{buildroot}%{_bindir} \
    SHAREZJS=%{buildroot}%{_datadir}/%{rname} \
    SHAREOAK=%{buildroot}%{_datadir}/foo2oak \
    SHAREHP=%{buildroot}%{_datadir}/foo2hp \
    SHAREXQX=%{buildroot}%{_datadir}/foo2xqx \
    SHARELAVA=%{buildroot}%{_datadir}/foo2lava \
    SHAREQPDL=%{buildroot}%{_datadir}/foo2qpdl \
    MANDIR=%{buildroot}%{_mandir} \
    DOCDIR=%{buildroot}%{_datadir}/doc/%{rname}/ \
    FOODB=%{buildroot}%{_datadir}/foomatic/db/source \
    MODEL=%{buildroot}%{_datadir}/cups/model/%{rname}

%if %mdkversion < 200700
install -m0755 msexpand %{buildroot}%{_bindir}
%endif

install -m0755 getweb %{buildroot}%{_bindir}/%{rname}-getweb

mv %{buildroot}%{_bindir}/usb_printerid %{buildroot}%{_sbindir}/usb_printerid

install -m0755 hplj1000 %{buildroot}%{_sbindir}/
perl -p -i -e 's:\./(getweb):%{rname}-$1:g' %{buildroot}%{_sbindir}/hplj1000
perl -p -i -e 's:/bin(/usb_printerid):%{_sbindir}$1:g' %{buildroot}%{_sbindir}/hplj1000

ln -s hplj1000 %{buildroot}%{_sbindir}/hplj1005
ln -s hplj1000 %{buildroot}%{_sbindir}/hplj1018
ln -s hplj1000 %{buildroot}%{_sbindir}/hplj1020

install -m0644 hplj10xx.rules %{buildroot}%{_sysconfdir}/udev/rules.d/70-hplj10xx.rules
perl -p -i -e 's:%{_sysconfdir}/hotplug/usb:%{_sbindir}:' %{buildroot}%{_sysconfdir}/udev/rules.d/70-hplj10xx.rules

ln -s /etc/printer %{buildroot}%{_datadir}/%{rname}/firmware
ln -s /etc/printer %{buildroot}%{_datadir}/firmware

# cleanup
rm -rf %{buildroot}%{_datadir}/doc/%{rname}

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc COPYING ChangeLog INSTALL INSTALL.usb README manual.pdf
%{_sysconfdir}/udev/rules.d/70-hplj10xx.rules
%attr(0755,root,root) %{_bindir}/arm2hpdl
%attr(0755,root,root) %{_bindir}/foo2hp
%attr(0755,root,root) %{_bindir}/foo2hp2600-wrapper
%attr(0755,root,root) %{_bindir}/foo2lava
%attr(0755,root,root) %{_bindir}/foo2lava-wrapper
%attr(0755,root,root) %{_bindir}/foo2oak-wrapper
%attr(0755,root,root) %{_bindir}/foo2qpdl
%attr(0755,root,root) %{_bindir}/foo2qpdl-wrapper
%attr(0755,root,root) %{_bindir}/foo2xqx
%attr(0755,root,root) %{_bindir}/foo2xqx-wrapper
%attr(0755,root,root) %{_bindir}/%{rname}
%attr(0755,root,root) %{_bindir}/%{rname}-getweb
%attr(0755,root,root) %{_bindir}/%{rname}-wrapper
%attr(0755,root,root) %{_bindir}/lavadecode
%attr(0755,root,root) %{_bindir}/opldecode
%attr(0755,root,root) %{_bindir}/qpdldecode
%attr(0755,root,root) %{_bindir}/xqxdecode
%attr(0755,root,root) %{_bindir}/zjsdecode

%if %mdkversion < 200700
%{_bindir}/msexpand
%endif

%attr(0755,root,root) %{_sbindir}/usb_printerid
%attr(0755,root,root) %{_sbindir}/hplj1000
%attr(0755,root,root) %{_sbindir}/hplj1005
%attr(0755,root,root) %{_sbindir}/hplj1018
%attr(0755,root,root) %{_sbindir}/hplj1020

%attr(0644,root,root) %{_mandir}/man1/foo2hp.1*
%attr(0644,root,root) %{_mandir}/man1/foo2hp2600-wrapper.1*
%attr(0644,root,root) %{_mandir}/man1/foo2lava.1*
%attr(0644,root,root) %{_mandir}/man1/foo2lava-wrapper.1*
%attr(0644,root,root) %{_mandir}/man1/foo2oak.1*
%attr(0644,root,root) %{_mandir}/man1/foo2oak-wrapper.1*
%attr(0644,root,root) %{_mandir}/man1/foo2qpdl.1*
%attr(0644,root,root) %{_mandir}/man1/foo2qpdl-wrapper.1*
%attr(0644,root,root) %{_mandir}/man1/foo2xqx.1*
%attr(0644,root,root) %{_mandir}/man1/foo2xqx-wrapper.1*
%attr(0644,root,root) %{_mandir}/man1/%{rname}.1*
%attr(0644,root,root) %{_mandir}/man1/%{rname}-wrapper.1*
%attr(0644,root,root) %{_mandir}/man1/lavadecode.1*
%attr(0644,root,root) %{_mandir}/man1/oakdecode.1*
%attr(0644,root,root) %{_mandir}/man1/opldecode.1*
%attr(0644,root,root) %{_mandir}/man1/qpdldecode.1*
%attr(0644,root,root) %{_mandir}/man1/xqxdecode.1*
%attr(0644,root,root) %{_mandir}/man1/zjsdecode.1*

%attr(0755,root,root) %dir %{_datadir}/foo2hp
%attr(0755,root,root) %dir %{_datadir}/foo2hp/icm
%attr(0755,root,root) %dir %{_datadir}/%{rname}
%attr(0755,root,root) %dir %{_datadir}/%{rname}/crd
%attr(0755,root,root) %dir %{_datadir}/%{rname}/firmware
%attr(0755,root,root) %dir %{_datadir}/%{rname}/icm
%attr(0755,root,root) %dir %{_datadir}/foo2xqx
%attr(0755,root,root) %dir %{_datadir}/foo2lava
%attr(0755,root,root) %dir %{_datadir}/foo2lava/icm
%attr(0755,root,root) %dir %{_datadir}/foo2oak
%attr(0755,root,root) %dir %{_datadir}/foo2oak/icm
%attr(0755,root,root) %dir %{_datadir}/foo2qpdl
%attr(0755,root,root) %dir %{_datadir}/foo2qpdl/crd
%attr(0755,root,root) %dir %{_datadir}/foo2qpdl/icm

%attr(0644,root,root) %{_datadir}/%{rname}/*.ps
%attr(0644,root,root) %{_datadir}/%{rname}/crd/*.crd
%attr(0644,root,root) %{_datadir}/%{rname}/crd/*.ps
%attr(0644,root,root) %{_datadir}/foo2qpdl/crd/*cms*
%attr(0644,root,root) %{_datadir}/foo2qpdl/crd/*.ps

%{_datadir}/firmware
%{_datadir}/%{rname}/firmware/printer

%attr(0644,root,root) %{_datadir}/foomatic/db/source/opt/*.xml
%attr(0644,root,root) %{_datadir}/foomatic/db/source/printer/*.xml
%attr(0644,root,root) %{_datadir}/foomatic/db/source/driver/*.xml

%attr(0755,root,root) %dir %{_datadir}/cups/model/%{rname}
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Generic-OAKT_Printer.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Generic-ZjStream_Printer.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-Color_LaserJet_1500.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-Color_LaserJet_1600.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-Color_LaserJet_2600n.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-LaserJet_1000.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-LaserJet_1005.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-LaserJet_1018.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-LaserJet_1020.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-LaserJet_1022.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/HP-LaserJet_M1005_MFP.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/KonicaMinolta-magicolor_2480_MF.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/KonicaMinolta-magicolor_2490_MF.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/KonicaMinolta-magicolor_2530_DL.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Minolta-Color_PageWorks_Pro_L.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Minolta-magicolor_2200_DL.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Minolta-magicolor_2300_DL.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Minolta-magicolor_2430_DL.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Samsung-CLP-300.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Samsung-CLP-600.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Samsung-CLX-3160.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Xerox-Phaser-6110.ppd*
%attr(0644,root,root) %{_datadir}/cups/model/%{rname}/Xerox-Phaser-6115MFP.ppd*
