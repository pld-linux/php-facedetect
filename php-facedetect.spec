#
# Conditional build:
%bcond_without	tests		# build without tests

%define		php_name	php%{?php_suffix}
%define		modname	facedetect
Summary:	PHP Facedetect Extension
Name:		%{php_name}-%{modname}
Version:	1.1
Release:	2
License:	PHP 3.0
Group:		Development/Languages/PHP
Source0:	https://github.com/infusion/PHP-Facedetect/tarball/master/%{modname}.tar.gz
# Source0-md5:	e76f2b1fd2b24a84f7123888f433f030
#Source0:	http://www.xarg.org/download/facedetect-%{version}.tar.gz
URL:		http://www.xarg.org/project/php-facedetect/
BuildRequires:	%{php_name}-devel
BuildRequires:	opencv-devel
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This extension provides a PHP implementation of the OpenCV library.
The extension offers two new functions. In princible, they differ only
by their return value. The first returns only the number of faces
found on the given image and the other an associative array of their
coordinates.

%prep
%setup -qc
mv infusion-PHP-Facedetect-4b1dfe1/* .

%build
export LIBS=%{_libdir}/libopencv_*.so.*
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_sysconfdir}/conf.d,%{php_extensiondir}}
%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc CREDITS
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
