Summary:	Improved SANE frontend
Summary(pl):	Ulepszony frontend do SANE
Summary(zh_CN): xsane - һ��ͼ��ɨ�����
Name:		xsane
Version:	0.87
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://www.xsane.org/download/%{name}-%{version}.tar.gz
Source1:	%{name}.desktop
Source2:	%{name}.png
Patch0:		%{name}-DESTDIR.patch
URL:		http://www.xsane.org/
BuildRequires:	autoconf
BuildRequires:	gimp-devel
BuildRequires:	gtk+-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtiff-devel
BuildRequires:	sane-backends-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_prefix		/usr/X11R6
%define		_mandir		%{_prefix}/man
%define		_gimpplugindir	%(gimp-config --gimpplugindir)/plug-ins

%description
XSane is a graphical scanning frontend. It uses the SANE library to
talk to scanner.

%description -l pl
XSane jest graficznym frontendem do skanowania. U�ywa biblioteki SANE
do komunikacji ze skanerem.

%prep
%setup -q
%patch0 -p1

%build
%{__autoconf}
if [ -f %{_pkgconfigdir}/libpng12.pc ] ; then
	CPPFLAGS="`pkg-config libpng12 --cflags`"
fi
%configure CPPFLAGS="$CPPFLAGS"
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_gimpplugindir},%{_applnkdir}/Graphics,%{_pixmapsdir}}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}/Graphics
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

ln -sf %{_bindir}/xsane $RPM_BUILD_ROOT%{_gimpplugindir}/xsane

gzip -9nf xsane.{ACCELKEYS,AUTHOR,BACKENDS,BUGS,CHANGES,LOGO,NEWS} \
	xsane.{PROBLEMS,TODO,BEGINNERS-INFO,ONLINEHELP}

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc *.gz
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_gimpplugindir}/*
%{_datadir}/sane
%{_mandir}/man1/*
%{_applnkdir}/Graphics/*
%{_pixmapsdir}/*
