%define obsprov licq-base licq-ssl licq-data licq-update-hosts licq-forwarder licq-autoreply licq-kde

Name:		licq
Version:	1.3.9
Release:	%mkrel 1
Summary:	ICQ clone written in C++
License:	GPLv2+
Group:		Networking/Instant messaging
URL:		http://www.licq.org/
Source0:	http://ovh.dl.sourceforge.net/licq/licq-%{version}.tar.bz2
Source1:	%{name}-other-browsers.tar.bz2
Source6:	forwarder-1.0.1.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch1:		licq-1.3.7-conf.patch
Patch2:		licq-1.3.4-xvt.patch
Patch5:		licq-1.3.0-c++fixes.patch 
Patch15:	licq-1.3.7-mdv-fix-str-fmt.patch
Obsoletes:	%{obsprov}
BuildRequires:	autoconf
BuildRequires:	qt4-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	cdk-devel >= 4.9.11-4mdk
BuildRequires:	gpgme-devel >= 0.9.0
BuildRequires:  automake
Requires:	licq-frontend = %version
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package	console
Summary:	Console based plugin for Licq that uses ncurses
Group:		Networking/Instant messaging
Provides:	licq-frontend = %version
Requires:	licq = %{version} ncurses

%package	qt4
Summary:	Qt4 plugin for Licq
Group:		Networking/Instant messaging
Provides:	licq-frontend = %version
Requires:	licq = %{version}
Conflicts:	licq < %{version}

%package	devel
Summary:	Development files for Licq
Group:		Development/C

%package	rms
Summary:	Remote management service Licq plugin
Group:		Networking/Instant messaging
Provides:	licq-plugin
Requires:	licq = %{version}

%description	devel
This is the header files that you will need in order to compile Licq plugins.

%description 
Licq supports different interfaces and functions via
plugins. Currently there are plugins for both the X Windowing System
and the console.

This version of licq has SSL support for those plugins that support it.

%description	rms
RMS stands for the Remote Management Service. It is a plugin for Licq
which enables you to "telnet" to your Licq box to perform various
tasks. Security is implemented through basic username and password
authentication.

%description	qt4
This package contains the base files for Licq (the Licq daemon) and
the Qt plugin, which is written using the Qt widget set. Currently
this GUI plugin has most of the ICQ functions implemented.

This starts the Qt plugin by default, so to run other plugins, you
will have to issue the command "licq -p <plugin>" once. To get back
the Qt plugin, you will have to run once "licq -p qt-gui".
Alternatively you may be able to do it in a plugin dialog box
if your plugin supports this feature.

%description	console
This is a console based plugin for Licq that uses ncurses that came in
the standard Licq source package. It is extremely usable and
functional, but it does not currently have support for gpm.

Install this if you want to run Licq on the console.

%prep
#Danny: Also unpack other-browser stuff:
%setup -q -a 1
%patch1 -p1 -b .licq_conf
%patch2 -p1
%patch5 -p1 -b .c++fixes
%patch15 -p1 -b .strfmt

%build
rm -rf `find -type d -name autom4te.cache`
#main licq stuff
autoconf
%configure2_5x --enable-shared --disable-static
%make

cd plugins

# console interface /w ncurses plugin
cd console*
aclocal && automake && autoconf
export LIBS="$LIBS -lm"
%configure2_5x
%make

# remote management service
cd ../rms*
aclocal && automake && autoconf
%configure2_5x
%make

# qt gui
cd ../qt4-gui*
%cmake_qt4 -DCMAKE_MODULE_LINKER_FLAGS='%{?!_disable_ld_as_needed: -Wl,--as-needed}'
%make

%install
rm -rf $RPM_BUILD_ROOT

#licq base
%{makeinstall_std}

#qt gui
cd plugins/qt4-gui*
%{makeinstall_std} -C build

# console ui
cd ../console*
%{makeinstall_std}

# remote management service
cd ../rms*
%{makeinstall_std}
cd ../..

ln -sf licq $RPM_BUILD_ROOT%{_bindir}/licq-ssl

%{find_lang} %{name}

%clean
rm -rf $RPM_BUILD_ROOT  

%if %mdkversion < 200900
%post
%{update_menus}
%endif

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/licq
%{_bindir}/licq-ssl
%dir %{_datadir}/licq
%{_datadir}/licq/translations
%{_datadir}/licq/utilities
%{_datadir}/licq/sounds
%doc doc/ upgrade/ README*

# qt frontend
%files qt4
%defattr(-,root,root)
%{_libdir}/licq/licq_qt4-gui.so
%{_datadir}/licq/qt4-gui
%{_datadir}/applications/*.desktop
%{_bindir}/viewurl*.sh

# devel
%files devel
%defattr(-,root,root)
%{_includedir}/licq

# console frontend
%files console
%defattr(-,root,root)
%{_libdir}/licq/licq*console*
%doc plugins/console*/README 

# remote management service
%files rms
%defattr(-,root,root)
%{_libdir}/licq/licq*rms*
%doc plugins/rms*/COPYING plugins/rms*/README 


%changelog
* Thu Nov 25 2010 Funda Wang <fwang@mandriva.org> 1.3.9-1mdv2011.0
+ Revision: 600930
- new verison 1.3.9

* Mon Apr 19 2010 Funda Wang <fwang@mandriva.org> 1.3.8-2mdv2010.1
+ Revision: 536633
- rebuild

* Mon Dec 14 2009 Funda Wang <fwang@mandriva.org> 1.3.8-1mdv2010.1
+ Revision: 478580
- new version 1.3.8

* Tue Nov 24 2009 Jérôme Brenier <incubusss@mandriva.org> 1.3.7-1mdv2010.1
+ Revision: 469821
- new version 1.3.7
- rediff P1 and P10
- drop P8 (merged upstream)
- fix str fmt (P15 added)

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Sun Oct 12 2008 Funda Wang <fwang@mandriva.org> 1.3.6-1mdv2009.1
+ Revision: 292628
- New version 1.3.6
- comply LIB_SUFFIX

* Fri Jul 04 2008 Funda Wang <fwang@mandriva.org> 1.3.5-3mdv2009.0
+ Revision: 231668
- add patch to fix logon
- add gcc43 patch from gentoo

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Mon May 12 2008 Nicolas Lécureuil <nlecureuil@mandriva.com> 1.3.5-2mdv2009.0
+ Revision: 206191
- fixed DoS vulnerability - CVE-2008-1996

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Wed Nov 28 2007 David Walluck <walluck@mandriva.org> 1.3.5-1mdv2008.1
+ Revision: 113616
- 1.3.5

* Tue Sep 18 2007 Guillaume Rousse <guillomovitch@mandriva.org> 1.3.4-2mdv2008.0
+ Revision: 89864
- rebuild

* Sun Sep 02 2007 Funda Wang <fwang@mandriva.org> 1.3.4-1mdv2008.0
+ Revision: 77738
- rediff patch2
- 64bit fix not needed
- New version 1.3.4


* Thu Jan 12 2006 Nicolas L�cureuil <neoclust@mandriva.org> 1.3.2-1mdk
- New release 1.3.2
- Rediff Patch 2
- Remove Patch 3 (Merged upstream) 
- Fix File List
- Add BuildRequires
- use mkrel

* Mon Nov 14 2005 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-7mdk
- rebuilt against openssl-0.9.8a

* Tue Aug 23 2005 Gwenole Beauchesne <gbeauchesne@mandriva.com> 1.3.0-6mdk
- c++ fixes

* Sat May 21 2005 Oden Eriksson <oeriksson@mandriva.com> 1.3.0-5mdk
- fix deps

* Fri Apr 15 2005 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.0-4mdk
- added P4 by Robert Schiele to make it compile against latest gpgme
- libcdk-devel requires to be build with -fPIC

* Wed Mar 16 2005 Oden Eriksson <oden.eriksson@kvikkjokk.net> 1.3.0-3mdk
- added BuildRequires: libgpgme03-devel
- make the console stuff compile

* Sun Nov 14 2004 Christiaan Welvaart <cjw@daneel.dyndns.org> 1.3.0-2mdk
- add BuildRequires: libcdk-devel

* Wed Nov 10 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.3.0-1mdk
- 1.3.0
- add locale files
- regenerate P1 & P3
- drop P4 (fixed upstream)

* Fri Aug 27 2004 Frederic Crozat <fcrozat@mandrakesoft.com> 1.2.7-3mdk
- Fix menu

* Tue Jun 15 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.2.7-2mdk
- rebuild

* Wed Jun 02 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 1.2.7-1mdk
- 1.2.7
- fix gcc3.4 build (P4 from fedora)
- do not bzip2 icons
- do libtoolize
- cleanups

* Thu Apr 15 2004 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.6-5mdk
- rebuild

* Wed Oct 01 2003 Gwenole Beauchesne <gbeauchesne@mandrakesoft.com> 1.2.6-4mdk
- lib64 fixes

* Sun Jul 20 2003 Stefan van der Eijk <stefan@eijk.nu> 1.2.6-3mdk
- BuildRequires

* Thu Jul 17 2003 David BAUDENS <baudens@mandrakesoft.com> 1.2.6-2mdk
- Rebuild

* Thu Apr 03 2003 Nicolas Planel <nplanel@mandrakesoft.com> 1.2.6-1mdk
- Bump to version 1.2.6.

* Wed Feb 19 2003 Chmouel Boudjnah <chmouel@mandrakesoft.com> 1.2.4-1mdk
- Bump to version 1.2.4.

