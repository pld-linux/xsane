Summary:	Improved SANE frontend
Summary(pl.UTF-8):	Ulepszony frontend do SANE
Summary(zh_CN.UTF-8):	xsane - 一个图形扫描程序
Name:		xsane
Version:	0.999
Release:	3
License:	GPL v2+
Group:		X11/Applications/Graphics
# Source0Download:	http://www.xsane.org/cgi-bin/sitexplorer.cgi?/download/
Source0:	http://www.xsane.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	9927f21e1ab6ba96315e7f0e30746deb
Source1:	%{name}.desktop
Source2:	%{name}.png
# from Fedora
Patch0:		%{name}-0.995-xdg-open.patch
Patch1:		%{name}-0.995-close-fds.patch
Patch2:		%{name}-0.996-no-eula.patch
Patch3:		%{name}-0.997-off-root-build.patch
Patch4:		%{name}-0.999-no-file-selected.patch
Patch5:		%{name}-0.997-ipv6.patch
Patch6:		%{name}-0.998-preview-selection.patch
Patch7:		%{name}-0.998-libpng.patch
Patch8:		%{name}-0.998-wmclass.patch
Patch9:		%{name}-0.998-desktop-file.patch
Patch10:	%{name}-0.999-man-page.patch
Patch11:	%{name}-0.999-pdf-no-high-bpp.patch
Patch12:	%{name}-0.999-lcms2.patch
Patch13:	%{name}-0.999-coverity.patch
Patch14:	%{name}-0.999-snprintf-update.patch
Patch15:	%{name}-0.999-signal-handling.patch
# PLD
Patch50:	%{name}-datadir.patch
Patch51:	%{name}-pl.po-update.patch
Patch52:	%{name}-poMakefile.patch
Patch53:	%{name}-build.patch
URL:		http://www.xsane.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-tools
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
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

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

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

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
