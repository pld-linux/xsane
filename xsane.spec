#
# Conditional build:
%bcond_with	gtk1	# use GTK+ 1.2 and GIMP 1.2 instead of GTK+ 2.0 and GIMP 2.0
#
Summary:	Improved SANE frontend
Summary(pl):	Ulepszony frontend do SANE
Summary(zh_CN):	xsane - һ��ͼ��ɨ�����
Name:		xsane
Version:	0.96
Release:	2
License:	GPL
Group:		X11/Applications/Graphics
#Source0Download:	http://www.xsane.org/cgi-bin/sitexplorer.cgi?/download/
Source0:	http://www.xsane.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	32e4693c207d0380436c76096f8c157c
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-datadir.patch
URL:		http://www.xsane.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
%if %{with gtk1}
BuildRequires:	gimp-devel >= 1.0.0
BuildRequires:	gtk+-devel >= 1.2.0
%else
BuildRequires:	gimp-devel >= 1:2.0.0
BuildRequires:	gtk+2-devel >= 1:2.0.0
%endif
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	sane-backends-devel >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gimpplugindir	%(gimptool --gimpplugindir)/plug-ins

%description
XSane is a graphical scanning frontend. It uses the SANE library to
talk to scanner.

%description -l pl
XSane jest graficznym frontendem do skanowania. U�ywa biblioteki SANE
do komunikacji ze skanerem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1

mv -f po/{sr,sr@Latn}.po
mv -f po/{zh,zh_TW}.po

%{__perl} -pi -e 's/ sr / sr\@Latn /;s/ zh/ zh_TW/' configure.in

%build
%{__gettextize}
%{__aclocal} -I m4
%{__autoconf}
%configure \
	%{?with_gtk1:--disable-gimp2} \
	%{?with_gtk1:--disable-gtk2}

# I don't really know why it desn't work without this one and
# I don't know how to fix it in the right way...
sed -ie '/^# Makevars gets/r po/Makevars' po/Makefile

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
%doc xsane.{ACCELKEYS,AUTHOR,BACKENDS,BUGS,CHANGES,LOGO,NEWS,PROBLEMS,TODO,BEGINNERS-INFO,ONLINEHELP}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_gimpplugindir}/*
%{_datadir}/xsane
%{_mandir}/man1/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*
