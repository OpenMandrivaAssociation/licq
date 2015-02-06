Summary:	ICQ clone written in C++
Name:		licq
Version:	1.8.2
Release:	2
License:	GPLv2+
Group:		Networking/Instant messaging
Url:		http://www.licq.org/
Source0:	http://ovh.dl.sourceforge.net/licq/%{name}-%{version}.tar.bz2
BuildRequires:	cmake
BuildRequires:	doxygen
BuildRequires:	boost-devel
BuildRequires:	cdk-devel
BuildRequires:	gpgme-devel
BuildRequires:	qt4-devel
BuildRequires:	pkgconfig(gloox)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(xscrnsaver)
Requires:	licq-frontend = %{EVRD}
Requires:	licq-protocol = %{EVRD}
Requires:	sox
# Seems to be dropped
Obsoletes:	licq-console < 1.8.2

%description
Licq supports different interfaces and functions via
plugins. Currently there are plugins for both the X Windowing System
and the console.

This version of licq has SSL support for those plugins that support it.

%files -f %{name}.lang
%doc doc/ upgrade/ README*
%{_bindir}/licq
%{_bindir}/licq-ssl
%dir %{_datadir}/licq
%{_datadir}/licq/translations
%{_datadir}/licq/utilities
%{_datadir}/licq/sounds

#----------------------------------------------------------------------------

%package qt4
Summary:	Qt4 plugin for Licq
Group:		Networking/Instant messaging
Provides:	licq-frontend = %{EVRD}
Requires:	%{name} = %{EVRD}

%description qt4
This package contains the base files for Licq (the Licq daemon) and
the Qt plugin, which is written using the Qt widget set. Currently
this GUI plugin has most of the ICQ functions implemented.

This starts the Qt plugin by default, so to run other plugins, you
will have to issue the command "licq -p <plugin>" once. To get back
the Qt plugin, you will have to run once "licq -p qt-gui".
Alternatively you may be able to do it in a plugin dialog box
if your plugin supports this feature.

%files qt4
%{_libdir}/licq/licq_qt4-gui.so
%{_datadir}/licq/qt4-gui
%{_datadir}/applications/*.desktop

#----------------------------------------------------------------------------

%package icq
Summary:	ICQ Licq plugin
Group:		Networking/Instant messaging
Provides:	licq-protocol = %{EVRD}
Requires:	%{name} = %{EVRD}

%description icq
ICQ plugin for Licq.

%files icq
%doc plugins/icq/README
%{_libdir}/licq/protocol_icq.so

#----------------------------------------------------------------------------

%package jabber
Summary:	Jabber Licq plugin
Group:		Networking/Instant messaging
Provides:	licq-protocol = %{EVRD}
Requires:	%{name} = %{EVRD}

%description jabber
ICQ plugin for Licq.

%files jabber
%doc plugins/jabber/README plugins/jabber/COPYING
%{_libdir}/licq/protocol_jabber.so

#----------------------------------------------------------------------------

%package rms
Summary:	Remote management service Licq plugin
Group:		Networking/Instant messaging
Requires:	%{name} = %{EVRD}

%description rms
RMS stands for the Remote Management Service. It is a plugin for Licq
which enables you to "telnet" to your Licq box to perform various
tasks. Security is implemented through basic username and password
authentication.

%files rms
%doc plugins/rms*/COPYING plugins/rms*/README
%{_libdir}/licq/licq*rms*

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for Licq
Group:		Development/C

%description devel
This is the header files that you will need in order to compile Licq plugins.

%files devel
%{_datadir}/cmake/Modules/*.cmake
%{_includedir}/licq

#----------------------------------------------------------------------------

%prep
%setup -q

%build
%cmake
%make
cd ..

cmakeopts="-DCMAKE_MODULE_PATH=%{_builddir}/%{name}-%{version}/cmake -DLicq_DIR=%{_builddir}/%{name}-%{version}/build/cmake"

# Qt4 gui
pushd plugins/qt4-gui
%cmake $cmakeopts
%make
popd

# Remote management service
pushd plugins/rms
%cmake $cmakeopts
%make
popd

# ICQ
pushd plugins/icq
%cmake $cmakeopts
%make
popd

# Jabber
pushd plugins/jabber
%cmake $cmakeopts
%make
popd

%install
%makeinstall_std -C build
%makeinstall_std -C plugins/qt4-gui/build
%makeinstall_std -C plugins/rms/build
%makeinstall_std -C plugins/icq/build
%makeinstall_std -C plugins/jabber/build

ln -sf licq %{buildroot}%{_bindir}/licq-ssl

# Fix cmake modules location
mkdir -p %{buildroot}%{_datadir}/cmake/Modules
mv %{buildroot}%{_datadir}/%{name}/cmake/*.cmake %{buildroot}%{_datadir}/cmake/Modules/
rm -rf %{buildroot}%{_datadir}/%{name}/cmake

%find_lang %{name}

