#
# Conditional build:
# _with_gtk1	- use GTK+ 1.2 and GIMP 1.2 instead of GTK+ 2.0 and GIMP 1.3
#
Summary:	Improved SANE frontend
Summary(pl):	Ulepszony frontend do SANE
Summary(zh_CN): xsane - 一个图形扫描程序
Name:		xsane
Version:	0.90
Release:	2
License:	GPL
Group:		X11/Applications/Graphics
#Source0Download:	http://www.xsane.org/cgi-bin/sitexplorer.cgi?/download/
Source0:	http://www.xsane.org/download/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-DESTDIR.patch
Patch1:		%{name}-gimp1.3.patch
URL:		http://www.xsane.org/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
%if 0%{?_with_gtk1:1}
BuildRequires:	gimp-devel >= 1.0.0
BuildRequires:	gtk+-devel >= 1.2.0
%else
BuildRequires:	gimp-devel >= 1.3.0
BuildRequires:	gtk+2-devel >= 2.0.0
%endif
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	sane-backends-devel >= 1.0.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_gimpplugindir	%(gimp-config --gimpplugindir)/plug-ins

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

%build
# AM_PATH_SANE
head -622 aclocal.m4 | tail +457 > acinclude.m4
%if 0%{?_with_gtk1:1}
echo 'AC_DEFUN([AM_PATH_GTK2],[])' >> acinclude.m4
%else
cat >> acinclude.m4 <<EOF
AC_DEFUN([AM_PATH_GTK],[true])
AC_DEFUN([AM_PATH_GTK2],[AM_PATH_GTK_2_0(\$1,\$2,\$3)])
AC_DEFUN([AM_PATH_GIMP],[
AM_PATH_GIMP_1_4(\$1,\$2)
save_CPPFLAGS="\$CPPFLAGS"
CPPFLAGS="\$CPPFLAGS \$GIMP_CFLAGS"
AC_CHECK_HEADERS([libgimp/gimp.h libgimp/gimpfeatures.h])
])
EOF
%endif
echo 'AC_DEFUN([AM_FUNC_ALLOCA],[AC_FUNC_ALLOCA])' >> acinclude.m4
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
install -d $RPM_BUILD_ROOT{%{_gimpplugindir},%{_applnkdir}/Graphics,%{_pixmapsdir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Graphics
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

ln -sf %{_bindir}/xsane $RPM_BUILD_ROOT%{_gimpplugindir}/xsane

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc xsane.{ACCELKEYS,AUTHOR,BACKENDS,BUGS,CHANGES,LOGO,NEWS}
%doc xsane.{PROBLEMS,TODO,BEGINNERS-INFO,ONLINEHELP}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_gimpplugindir}/*
%{_datadir}/sane
%{_mandir}/man1/*
%{_applnkdir}/Graphics/*
%{_pixmapsdir}/*
