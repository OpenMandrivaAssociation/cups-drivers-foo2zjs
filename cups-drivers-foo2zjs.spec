%define rname foo2zjs
%define snap 20090122

Summary:	A linux printer driver for ZjStream protocol
Name:		cups-drivers-%{rname}
Version:	0.0
Release:	%mkrel 0.%{snap}.1
Group:		System/Printing
License:	GPL
URL:		http://foo2zjs.rkkda.com/
Source0:	http://foo2zjs.rkkda.com/foo2zjs.tar.gz
Patch0:		foo2zjs-system_icc2ps.diff
Patch2:		foo2zjs-cflags.diff
Patch3:		foo2zjs-system_jbig.diff
Patch4:		foo2zjs-LDFLAGS.diff
BuildRequires:	lcms
BuildRequires:	ghostscript
BuildRequires:	foomatic-filters
BuildRequires:	jbig-devel
Requires:	lcms
Requires:	wget
Requires:	foomatic-db-engine
# psutils, unzip, and mscompress needed by the foo2zjs driver
Requires:	psutils, unzip
Requires:	mscompress
Conflicts:	cups-drivers = 2007
Conflicts:	printer-utils = 2007
Conflicts:	printer-filters = 2007
Conflicts:	foomatic-db < 1:3.0.2-1.20070820.1mdv2008.0
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
foo2zjs is an open source printer driver for printers that use the Zenographics
ZjStream wire protocol for their print data, such as the Minolta/QMS magicolor
2300 DL. These printers are often erroneously referred to as winprinters or GDI
printers. Please read the README file for a list of supported printers.

%prep

%setup -q -n %{rname}
%patch0 -p1
%patch2 -p0
%patch3 -p0
%patch4 -p0

# fix attribs
chmod 644 COPYING ChangeLog INSTALL INSTALL.usb README

%build
make CFLAGS="%{optflags}" LDFLAGS="%{ldflags}"

# Fit udev rules to stricter syntax of new udev
# (blino) don't try to rename the device,
#         it has already been renamed to the exact same name in 50-mdk.rules
#         so udev would skip the rule
#perl -p -i -e 's:(KERNEL|BUS|SYSFS.*?)=([^=]):$1==$2:g;s{SYMLINK=}{SYMLINK+=}g;s{(?:NAME|MODE)=.*?,\s*}{}g;s:===:==:g' hplj10xx.rules

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_datadir}/foomatic/db/source/{driver,opt,printer}
install -d %{buildroot}%{_datadir}/cups/model/%{rname}
#install -d %{buildroot}%{_sysconfdir}/udev/rules.d

make install \
    DESTDIR="%{buildroot}" \
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

# bork, bork, bork
mv %{buildroot}/bin/usb_printerid %{buildroot}%{_bindir}/

install -m0755 getweb %{buildroot}%{_bindir}/%{rname}-getweb

mv %{buildroot}%{_bindir}/usb_printerid %{buildroot}%{_sbindir}/usb_printerid

install -m0755 hplj1000 %{buildroot}%{_sbindir}/
perl -p -i -e 's:\./(getweb):%{rname}-$1:g' %{buildroot}%{_sbindir}/hplj1000
perl -p -i -e 's:/bin(/usb_printerid):%{_sbindir}$1:g' %{buildroot}%{_sbindir}/hplj1000

ln -s hplj1000 %{buildroot}%{_sbindir}/hplj1005
ln -s hplj1000 %{buildroot}%{_sbindir}/hplj1018
ln -s hplj1000 %{buildroot}%{_sbindir}/hplj1020

#install -m0644 hplj10xx.rules %{buildroot}%{_sysconfdir}/udev/rules.d/70-hplj10xx.rules
#perl -p -i -e 's:%{_sysconfdir}/hotplug/usb:%{_sbindir}:' %{buildroot}%{_sysconfdir}/udev/rules.d/70-hplj10xx.rules

mkdir -p %{buildroot}%{_datadir}/%{name}/firmware

# cleanup
rm -rf %{buildroot}%{_datadir}/doc/%{rname}

# provided by foomatic-db
rm %{buildroot}/%{_datadir}/foomatic/db/source/printer/Generic-OAKT_Printer.xml

%clean
rm -rf %{buildroot}

%files
%defattr(0644,root,root,0755)
%doc COPYING ChangeLog INSTALL INSTALL.usb README manual.pdf
#%{_sysconfdir}/udev/rules.d/70-hplj10xx.rules
%{_mandir}/man1/arm2hpdl.1*
%{_mandir}/man1/foo2hiperc.1*
%{_mandir}/man1/foo2hiperc-wrapper.1*
%{_mandir}/man1/foo2hp.1*
%{_mandir}/man1/foo2hp2600-wrapper.1*
%{_mandir}/man1/foo2lava.1*
%{_mandir}/man1/foo2lava-wrapper.1*
%{_mandir}/man1/foo2oak.1*
%{_mandir}/man1/foo2oak-wrapper.1*
%{_mandir}/man1/foo2qpdl.1*
%{_mandir}/man1/foo2qpdl-wrapper.1*
%{_mandir}/man1/foo2slx.1*
%{_mandir}/man1/foo2slx-wrapper.1*
%{_mandir}/man1/foo2xqx.1*
%{_mandir}/man1/foo2xqx-wrapper.1*
%{_mandir}/man1/foo2zjs-pstops.1*
%{_mandir}/man1/hipercdecode.1*
%{_mandir}/man1/lavadecode.1*
%{_mandir}/man1/oakdecode.1*
%{_mandir}/man1/opldecode.1*
%{_mandir}/man1/qpdldecode.1*
%{_mandir}/man1/%{rname}.1*
%{_mandir}/man1/%{rname}-wrapper.1*
%{_mandir}/man1/slxdecode.1*
%{_mandir}/man1/usb_printerid.1*
%{_mandir}/man1/xqxdecode.1*
%{_mandir}/man1/zjsdecode.1*

%dir %{_datadir}/foo2hp
%dir %{_datadir}/foo2hp/icm
%dir %{_datadir}/%{rname}
%dir %{_datadir}/%{rname}/crd
%dir %{_datadir}/%{rname}/firmware
%dir %{_datadir}/%{rname}/icm
%dir %{_datadir}/foo2xqx
%dir %{_datadir}/foo2lava
%dir %{_datadir}/foo2lava/icm
%dir %{_datadir}/foo2oak
%dir %{_datadir}/foo2oak/icm
%dir %{_datadir}/foo2qpdl
%dir %{_datadir}/foo2qpdl/crd
%dir %{_datadir}/foo2qpdl/icm

%{_datadir}/%{rname}/*.ps
%{_datadir}/%{rname}/crd/*.crd
%{_datadir}/%{rname}/crd/*.ps
%{_datadir}/foo2qpdl/crd/*cms*
%{_datadir}/foo2qpdl/crd/*.ps

%{_datadir}/foomatic/db/source/opt/*.xml
%{_datadir}/foomatic/db/source/printer/*.xml
%{_datadir}/foomatic/db/source/driver/*.xml

%dir %{_datadir}/cups/model/%{rname}
%{_datadir}/cups/model/%{rname}/Generic-OAKT_Printer.ppd*
%{_datadir}/cups/model/%{rname}/Generic-ZjStream_Printer.ppd*
%{_datadir}/cups/model/%{rname}/HP-Color_LaserJet_1500.ppd*
%{_datadir}/cups/model/%{rname}/HP-Color_LaserJet_1600.ppd*
%{_datadir}/cups/model/%{rname}/HP-Color_LaserJet_2600n.ppd*
%{_datadir}/cups/model/%{rname}/HP-Color_LaserJet_CP1215.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_1000.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_1005.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_1018.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_1020.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_1022.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_M1005_MFP.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_M1120_MFP.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_M1319_MFP.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_P1005.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_P1006.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_P1007.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_P1008.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_P1505.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_P2014.ppd*
%{_datadir}/cups/model/%{rname}/HP-LaserJet_P2035.ppd*
%{_datadir}/cups/model/%{rname}/KONICA_MINOLTA-magicolor_2480_MF.ppd*
%{_datadir}/cups/model/%{rname}/KONICA_MINOLTA-magicolor_2490_MF.ppd*
%{_datadir}/cups/model/%{rname}/KONICA_MINOLTA-magicolor_2530_DL.ppd*
%{_datadir}/cups/model/%{rname}/Kyocera-KM-1635.ppd*
%{_datadir}/cups/model/%{rname}/Kyocera-KM-2035.ppd*
%{_datadir}/cups/model/%{rname}/Lexmark-C500.ppd.gz
%{_datadir}/cups/model/%{rname}/Minolta-Color_PageWorks_Pro_L.ppd*
%{_datadir}/cups/model/%{rname}/Minolta-magicolor_2200_DL.ppd*
%{_datadir}/cups/model/%{rname}/Minolta-magicolor_2300_DL.ppd*
%{_datadir}/cups/model/%{rname}/Minolta-magicolor_2430_DL.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C3100.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C3200.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C3300.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C3400.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C3530_MFP.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C5100.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C5200.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C5500.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C5600.ppd*
%{_datadir}/cups/model/%{rname}/Oki-C5800.ppd*
%{_datadir}/cups/model/%{rname}/Samsung-CLP-300.ppd*
%{_datadir}/cups/model/%{rname}/Samsung-CLP-315.ppd*
%{_datadir}/cups/model/%{rname}/Samsung-CLP-600.ppd*
%{_datadir}/cups/model/%{rname}/Samsung-CLP-610.ppd*
%{_datadir}/cups/model/%{rname}/Samsung-CLX-2160.ppd*
%{_datadir}/cups/model/%{rname}/Samsung-CLX-3160.ppd*
%{_datadir}/cups/model/%{rname}/Samsung-CLX-3175.ppd*
%{_datadir}/cups/model/%{rname}/Xerox-Phaser_6110.ppd*
%{_datadir}/cups/model/%{rname}/Xerox-Phaser_6115MFP.ppd*

%{_datadir}/foo2zjs/hplj1020_icon.gif
%{_datadir}/foo2zjs/hplj10xx_gui.tcl

%defattr(0755,root,root,0755)
%{_bindir}/%{rname}
%{_bindir}/%{rname}-getweb
%{_bindir}/%{rname}-wrapper
%{_bindir}/arm2hpdl
%{_bindir}/foo2hiperc
%{_bindir}/foo2hiperc-wrapper
%{_bindir}/foo2hp
%{_bindir}/foo2hp2600-wrapper
%{_bindir}/foo2lava
%{_bindir}/foo2lava-wrapper
%{_bindir}/foo2oak
%{_bindir}/foo2oak-wrapper
%{_bindir}/foo2qpdl
%{_bindir}/foo2qpdl-wrapper
%{_bindir}/foo2slx
%{_bindir}/foo2slx-wrapper
%{_bindir}/foo2xqx
%{_bindir}/foo2xqx-wrapper
%{_bindir}/foo2zjs-pstops
%{_bindir}/gipddecode
%{_bindir}/hipercdecode
%{_bindir}/lavadecode
%{_bindir}/oakdecode
%{_bindir}/opldecode
%{_bindir}/qpdldecode
%{_bindir}/slxdecode
%{_bindir}/xqxdecode
%{_bindir}/zjsdecode
%{_sbindir}/usb_printerid
%{_sbindir}/hplj1000
%{_sbindir}/hplj1005
%{_sbindir}/hplj1018
%{_sbindir}/hplj1020


