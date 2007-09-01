%define name	licq
%define version	1.3.4
%define release %mkrel 1
%define obsprov licq-base licq-ssl licq-data licq-update-hosts licq-forwarder licq-autoreply

Summary:	ICQ clone written in C++, and the default plugin in Qt
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Networking/Instant messaging
URL:		http://www.licq.org/
Source0:	http://download.sourceforge.net/licq/%{name}-%{version}.tar.bz2
Source1:	%{name}-other-browsers.tar.bz2
Source6:	forwarder-1.0.1.tar.bz2
Source11:	%{name}.16.png
Source12:	%{name}.32.png
Source13:	%{name}.48.png
Patch1:		licq-1.3.0-conf.patch
Patch2:		licq-1.3.4-xvt.patch

Patch5:		licq-1.3.0-c++fixes.patch 
Obsoletes:	%{obsprov}
Provides:	%{obsprov}
BuildRequires:	autoconf2.5
BuildRequires:	kdelibs-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	cdk-devel >= 4.9.11-4mdk
BuildRequires:	gpgme-devel >= 0.9.0
BuildRequires:  automake
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%package	console
Summary:	Console based plugin for Licq that uses ncurses
Group:		Networking/Instant messaging
Provides:	licq-plugin
Requires:	licq = %{version} ncurses

%package	kde
Summary:	KDE-enabled Qt plugin for Licq
Group:		Networking/Instant messaging
Provides:	licq-plugin
Requires:	licq = %{version}

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

This package contains the base files for Licq (the Licq daemon) and
the Qt plugin, which is written using the Qt widget set. Currently
this GUI plugin has most of the ICQ functions implemented.

This starts the Qt plugin by default, so to run other plugins, you
will have to issue the command "licq -p <plugin>" once. To get back
the Qt plugin, you will have to run once "licq -p qt-gui".
Alternatively you may be able to do it in a plugin dialog box
if your plugin supports this feature.

This version of licq has SSL support for those plugins that support it.

%description	rms
RMS stands for the Remote Management Service. It is a plugin for Licq
which enables you to "telnet" to your Licq box to perform various
tasks. Security is implemented through basic username and password
authentication.

%description	kde
This is the KDE-enabled plugin for Licq. It is exactly the same as the
stock Qt GUI but it has some nice extra KDE specific stuff.

%description	console
This is a console based plugin for Licq that uses ncurses that came in
the standard Licq source package. It is extremely usable and
functional, but it does not currently have support for gpm.

Install this if you want to run Licq on the console.

%prep
#Danny: Also unpack other-browser stuff:
%setup -q -a 1
%patch1 -p1
%patch2 -p1
%patch5 -p1 -b .c++fixes

%build
# qt3 stuff
export QTDIR=%{_prefix}/lib/qt3
export QTLIB=$QTDIR/%{_lib}

export WANT_AUTOCONF_2_5=1
rm -rf `find -type d -name autom4te.cache`
#main licq stuff
autoconf
%configure2_5x
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


cp -Rf ../qt-gui* ../kde-gui

# kde gui
cd ../kde-gui*
rm -rf autom4te.cache

aclocal
autoconf
# Search for qt/kde libraries in the right directories (avoid patch)
# NOTE: please don't regenerate configure scripts below
perl -pi -e "s@/lib(\"|\b[^/])@/%_lib\1@g if /(kde|qt)_(libdirs|libraries)=/" configure
%configure2_5x --with-kde 
%make

# qt gui
cd ../qt-gui*
#danny: needed to run aclocal:
aclocal && automake --foreign --gnu && autoconf
%configure2_5x
# thanks to a buggy build system ..
pushd src
for i in *.h; do
${QTDIR}/bin/moc $i -o $(basename $i .h).moc || true
done
popd
%make


%install
rm -rf $RPM_BUILD_ROOT

#licq base
%{makeinstall_std}

mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_iconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}

install -m644 %{SOURCE11} -D $RPM_BUILD_ROOT%{_miconsdir}/licq.png
install -m644 %{SOURCE12} -D $RPM_BUILD_ROOT%{_iconsdir}/licq.png
install -m644 %{SOURCE13} -D $RPM_BUILD_ROOT%{_liconsdir}/licq.png


#qt gui
cd plugins/qt-gui*
mkdir -p $RPM_BUILD_ROOT%_datadir/licq/qt-gui/dock.{console,flower,flower-ns,glicq,kde2,pli}
%{makeinstall_std}

# kde gui
cd ../kde-gui*
install -m755 src/.libs/licq_kde-gui.so $RPM_BUILD_ROOT%{_libdir}/licq/licq_kde-gui.so
install -m644 src/.libs/licq_kde-gui.la $RPM_BUILD_ROOT%{_libdir}/licq/licq_kde-gui.la

# console ui
cd ../console*
%{makeinstall_std}

# remote management service
cd ../rms*
%{makeinstall_std}
cd ../..

ln -sf licq $RPM_BUILD_ROOT%{_bindir}/licq-ssl

find $RPM_BUILD_ROOT%{_datadir} -type d -exec chmod 755 {} \;

# remove dangling symlink.
rm -rf $RPM_BUILD_ROOT%{_datadir}/licq/qt-gui/locale/*

%{find_lang} %{name}

%clean
rm -rf $RPM_BUILD_ROOT  

%post
%{update_menus}

%postun
%{clean_menus}

#licq 
%files -f %{name}.lang
%defattr(-,root,root)
%{_bindir}/licq
%{_bindir}/licq-ssl
%{_bindir}/viewurl*.sh
%attr(755,root,root)%dir %{_datadir}/licq/qt-gui
%attr(755,root,root) %dir %{_datadir}/licq/translations
%attr(755,root,root) %dir %{_datadir}/licq/utilities
%attr(755,root,root) %dir %{_datadir}/licq/sounds
%{_datadir}/applications/*.desktop
%dir %_libdir/licq
%{_datadir}/licq/qt-gui/*
%{_datadir}/licq/sounds/*
%{_datadir}/licq/translations/*
%{_datadir}/licq/utilities/*.utility
%{_miconsdir}/licq.png
%{_iconsdir}/licq.png
%{_liconsdir}/licq.png
%{_libdir}/licq/licq*qt*
%doc doc/ upgrade/ README*

# kde gui
%files kde
%defattr(-,root,root)
%{_libdir}/licq/licq*kde*
%doc plugins/kde-gui*/doc/README*

# devel
%files devel
%defattr(-,root,root)
%{_includedir}/licq


#console plugin
%files console
%defattr(-,root,root)
%{_libdir}/licq/licq*console*
%doc plugins/console*/README 
# Danny: dissappeared: plugins/console*/licq_console.conf


# remote management service
%files rms
%defattr(-,root,root)
%{_libdir}/licq/licq*rms*
%doc plugins/rms*/COPYING plugins/rms*/README 
#Danny: seems to be gone: plugins/rms*/licq_rms.conf

