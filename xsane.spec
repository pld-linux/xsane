#
# Conditional build:
%bcond_with	gtk1	# use GTK+ 1.2 and GIMP 1.2 instead of GTK+ 2.0 and GIMP 1.3
#
Summary:	Improved SANE frontend
Summary(pl):	Ulepszony frontend do SANE
Summary(zh_CN): xsane - 一个图形扫描程序
Name:		xsane
Version:	0.92
Release:	7
License:	GPL
Group:		X11/Applications/Graphics
#Source0Download:	http://www.xsane.org/cgi-bin/sitexplorer.cgi?/download/
Source0:	http://www.xsane.org/download/%{name}-%{version}.tar.gz
# Source0-md5:	a5504d63cc5c9edb9ec484bd74581177
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-DESTDIR.patch
# based on http://people.debian.org/~jblache/misc/xsane-0.92_gimp2.0.patch
Patch1:		%{name}-gimp1.3.patch
Patch2:		%{name}-po.patch
Patch3:		%{name}-datadir.patch
URL:		http://www.xsane.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
%if %{with gtk1}
BuildRequires:	gimp-devel >= 1.0.0
BuildRequires:	gtk+-devel >= 1.2.0
%else
BuildRequires:	gimp-devel >= 1:1.3.23
BuildRequires:	gtk+2-devel >= 2.0.0
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
XSane jest graficznym frontendem do skanowania. U縴wa biblioteki SANE
do komunikacji ze skanerem.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1

mv -f po/{sr,sr@Latn}.po
mv -f po/{zh,zh_TW}.po

%{__perl} -pi -e 's/ sr / sr\@Latn /;s/ zh/ zh_TW/' configure.in

# AM_PATH_SANE
head -n 622 aclocal.m4 | tail -n +457 > acinclude.m4
%if %{with gtk1}
cat >> acinclude.m4 <<EOF
AC_DEFUN([AM_PATH_GTK2],[])
AC_DEFUN([AM_PATH_GIMP_2_0],[])
EOF
%else
cat >> acinclude.m4 <<EOF
AC_DEFUN([AM_PATH_GTK],[])
AC_DEFUN([AM_PATH_GIMP],[])
AC_DEFUN([AM_PATH_GTK2],[AM_PATH_GTK_2_0(\$1,\$2,\$3)])
])
EOF
%endif

%build
cp -f /usr/share/automake/config.* .
touch po/POTFILES.in
%{__gettextize}
%{__aclocal}
%{__autoconf}
# some gettext-w/o-automake issues require passing absolute srcdir :o
%configure \
	--srcdir=`pwd`
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
