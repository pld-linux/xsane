Summary:	Improved SANE frontend
Summary(pl.UTF-8):	Ulepszony frontend do SANE
Summary(zh_CN.UTF-8):	xsane - 一个图形扫描程序
Name:		xsane
Version:	0.999
Release:	3
License:	GPL v2+
Group:		X11/Applications/Graphics
#Source0Download:	http://www.xsane.org/cgi-bin/sitexplorer.cgi?/download/
Source0:	http://www.xsane.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	9927f21e1ab6ba96315e7f0e30746deb
Source1:	%{name}.desktop
Source2:	%{name}.png
# from Fedora
# use "xdg-open" instead of "netscape" to launch help browser
# submitted to upstream (Oliver Rauch) via email, 2013-06-04
Patch0: xsane-0.995-xdg-open.patch
# submitted to upstream (Oliver Rauch) via email, 2009-08-18
Patch1: xsane-0.995-close-fds.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=504344
# distro-specific(?), upstream won't accept it: "don't show license dialog"
# submitted to upstream (Oliver Rauch) anyway via email, 2013-06-04
Patch2: xsane-0.996-no-eula.patch
# enable off-root building
# submitted to upstream (Oliver Rauch) via email, 2010-06-23
Patch3: xsane-0.997-off-root-build.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=608047
# https://bugzilla.redhat.com/show_bug.cgi?id=621778
# submitted to upstream (Oliver Rauch) via email, 2013-07-05
Patch4: xsane-0.999-no-file-selected.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=198422
# submitted to upstream (Oliver Rauch) via email, 2010-06-29
Patch5: xsane-0.997-ipv6.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=624190
# fix from: https://bugs.launchpad.net/ubuntu/+source/xsane/+bug/370818
# submitted to upstream (Oliver Rauch) via email, 2011-06-01
Patch6: xsane-0.998-preview-selection.patch
# fix building with libpng >= 1.5
# submitted to upstream (Oliver Rauch) via email, 2011-11-21
Patch7: xsane-0.998-libpng.patch
# https://bugzilla.redhat.com/show_bug.cgi?id=795085
# set program name/wmclass so GNOME shell picks appropriate high resolution
# icon file
# submitted to upstream (Oliver Rauch) via email, 2013-06-04
Patch8: xsane-0.998-wmclass.patch
# partly distro-specific: customize desktop file
# submitted to upstream (Oliver Rauch) via email, 2013-06-04
Patch9: xsane-0.998-desktop-file.patch
# man page: update command line options
# submitted to upstream (Oliver Rauch) via email, 2013-07-08
Patch10: xsane-0.999-man-page.patch
# avoid producing PDFs with bpp > 8
# submitted to upstream (Oliver Rauch) via email, 2013-09-09
Patch11: xsane-0.999-pdf-no-high-bpp.patch
# build against lcms 2.x
# submitted to upstream (Oliver Rauch) via email, 2013-09-23
Patch12: xsane-0.999-lcms2.patch
# fix issues found during static analysis that don't require far-reaching
# refactoring
# submitted to upstream (Oliver Rauch) via email, 2014-04-02
Patch13: xsane-0.999-coverity.patch
# update lib/snprintf.c to the latest version from LPRng that has a Free license
# submitted to upstream (Oliver Rauch) via email, 2014-05-29
Patch14: xsane-0.999-snprintf-update.patch
# fix signal handling (#1073698)
# submitted to upstream (Oliver Rauch) via email, 2014-07-03
Patch15: xsane-0.999-signal-handling.patch

# PLD
Patch50:		%{name}-datadir.patch
Patch51:		%{name}-pl.po-update.patch
Patch52:		%{name}-poMakefile.patch
Patch53:		%{name}-build.patch
URL:		http://www.xsane.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gimp-devel >= 1:2.0.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	lcms2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	pkgconfig
BuildRequires:	sane-backends-devel >= 1.0.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gimpplugindir	%(gimptool --gimpplugindir 2>/dev/null)/plug-ins

%description
XSane is a graphical scanning frontend. It uses the SANE library to
talk to scanner.

%description -l pl.UTF-8
XSane jest graficznym frontendem do skanowania. Używa biblioteki SANE
do komunikacji ze skanerem.

%prep
%setup -q
%patch0 -p1 -b .xdg-open
%patch1 -p1 -b .close-fds
%patch2 -p1 -b .no-eula
%patch3 -p1 -b .off-root-build
%patch4 -p1 -b .no-file-selected
%patch5 -p1 -b .ipv6
%patch6 -p1 -b .preview-selection.patch
%patch7 -p1 -b .libpng
%patch8 -p1 -b .wmclass
%patch9 -p1 -b .desktop-file
%patch10 -p1 -b .man-page
%patch11 -p1 -b .pdf-no-high-bpp
%patch12 -p1 -b .lcms2
%patch13 -p1 -b .coverity
%patch14 -p1 -b .snprintf-update
%patch15 -p1 -b .signal-handling

%patch50 -p1
%patch51 -p1
%patch52 -p1
%patch53 -p1

mv -f po/{zh,zh_TW}.po

%{__sed} -i -e 's/ zh/ zh_TW/' configure.in

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_gimpplugindir},%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

ln -sf %{_bindir}/xsane $RPM_BUILD_ROOT%{_gimpplugindir}/xsane

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc ICM.TODO xsane.{ACCELKEYS,AUTHOR,BUGS,CHANGES,LOGO,NEWS,ONLINEHELP,PROBLEMS,ROOT,TODO}
%attr(755,root,root) %{_bindir}/xsane
%attr(755,root,root) %{_gimpplugindir}/xsane
%{_datadir}/xsane
%{_mandir}/man1/xsane.1*
%{_desktopdir}/xsane.desktop
%{_pixmapsdir}/xsane.png
