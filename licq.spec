%define obsprov licq-base licq-ssl licq-data licq-update-hosts licq-forwarder licq-autoreply licq-kde

Name:		licq
Version:	1.3.8
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
# fwang: this is solved in other ways upstream
Patch10:	licq-1.3.7-fix-desktop.patch
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
%patch10 -p1 -b .fixdesktop
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
