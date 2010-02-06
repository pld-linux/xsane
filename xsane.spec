Summary:	Improved SANE frontend
Summary(pl.UTF-8):	Ulepszony frontend do SANE
Summary(zh_CN.UTF-8):	xsane - 一个图形扫描程序
Name:		xsane
Version:	0.997
Release:	0.1
License:	GPL v2+
Group:		X11/Applications/Graphics
#Source0Download:	http://www.xsane.org/cgi-bin/sitexplorer.cgi?/download/
Source0:	http://www.xsane.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	8377b3e3b792f3d2b7f13895467c7082
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-datadir.patch
Patch1:		%{name}-pl.po-update.patch
Patch2:		%{name}-poMakefile.patch
URL:		http://www.xsane.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	gimp-devel >= 1:2.0.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
BuildRequires:	lcms-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	sane-backends-devel >= 1.0.0
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gimpplugindir	%(gimptool --gimpplugindir)/plug-ins

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
