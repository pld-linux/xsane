Summary:	XSANE --- GTK based SANE frontend
Summary(pl):	XSANE --- Interfejs do SANE oparty o GTK
Name:		xsane
Version:	0.57
Release:	0
Group:		Applications/Graphics
Group(pl):	Aplikacje/Grafika
Copyright:	GPL
Source0:	ftp://ftp.de.mostang.com/pub/sane/xsane/%{name}-%{version}.tar.gz
Patch0:	%{name}-DESTDIR.patch
URL:		http://www.mostang.com/sane/
BuildRequires:	XFree86-devel
BuildRequires:	glib-devel
BuildRequires:	gtk+-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	gimp-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define _prefix /usr/X11R6

%description
xsane provides a graphical user-interface  to  control  an
image  acquisition  device  such as a flatbed scanner.  It
allows previewing and scanning invidual images and can  be
invoked  either  directly from the command-line or through
The GIMP image manipulation program.  In the former  case,
xsane  acts  as  a stand-alone program that saves acquired
images in a suitable PNM format (PBM  for  black-and-white
images,  PGM  for  grayscale  images,  and  PPM  for color
images) or converts the image to JPEG, PNG,  PS  or  TIFF.
In  the latter case, the images are directly passed to The
GIMP for further processing.

%prep
%setup  -q
%patch0 -p1

%build
LDFLAGS="-s" ; export LDFLAGS
CFLAGS="$RPM_OPT_FLAGS" ; export CFLAGS
%configure 
make

%install
rm -rf "$RPM_BUILD_ROOT"

make install DESTDIR="$RPM_BUILD_ROOT"

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man*/* \
	xsane.{AUTHOR,BACKENDS,BUGS,CHANGES,LANGUAGES,LOGO,NEWS,ONLINEHELP,PROBLEMS,TODO,WIP} || :

install -d $RPM_BUILD_ROOT/usr/X11R6/lib/gimp/1.1/plug-ins/
ln -s ../../../../bin/xsane "$RPM_BUILD_ROOT"/usr/X11R6/lib/gimp/1.1/plug-ins/

%find_lang %{name}

%pre

%preun

%post

%postun
 
%clean
rm -rf "$RPM_BUILD_ROOT"

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc xsane.{AUTHOR,BACKENDS,BUGS,CHANGES,LANGUAGES,LOGO,NEWS,ONLINEHELP,PROBLEMS,TODO,WIP}.gz
%{_datadir}/sane
%{_mandir}/man1/*
%attr(755,root,root) %{_bindir}/*
/usr/X11R6/lib/gimp/1.1/plug-ins/*
