Summary:	improved SANE frontend
Summary(pl):	poprawiony frontend do SANE
Name:		xsane
Version:	0.72
Release:	1
Group:		X11/Applications/Graphics
License:	GPL
Source0:	http://www.xsane.org/download/%{name}-%{version}.tar.gz
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.xsane.org
BuildRequires:	sane-backends-devel
BuildRequires:	gimp-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	gtk+-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define	_prefix	/usr/X11R6
%define _mandir	/usr/X11R6/man

%description
XSane is a graphical scanning frontend. It uses the SANE library to talk to
scanner.

%description -l pl
XSane jest graficznym frontendem do skanowania. U¿ywa biblioteki SANE
do komunikacji ze skanerem.

%prep
%setup -q
%patch0 -p1

%build
autoconf
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_libdir}/gimp/%{gimp_ver}/plug-ins
ln -sf /usr/X11R6/bin/xsane $RPM_BUILD_ROOT%{_libdir}/gimp/%{gimp_ver}/plug-ins/xsane

gzip -9nf xsane.{ACCELKEYS,AUTHOR,BACKENDS,BUGS,CHANGES,LOGO,NEWS} \
	xsane.{PROBLEMS,TODO,WIP}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_datadir}/sane/*
%attr(755,root,root) %{_libdir}/gimp/%{gimp_ver}/plug-ins/*
%{_mandir}/man1/*
