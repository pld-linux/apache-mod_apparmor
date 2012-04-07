%define		mod_name	apparmor
%define 	apxs		/usr/sbin/apxs
Summary:	Apache module: AppArmor
Summary(pl.UTF-8):	Moduł Apache'a: AppArmor
Name:		apache-mod_%{mod_name}
Version:	2.7.2
Release:	1
Epoch:		1
License:	LGPL v2.1
Group:		Networking/Daemons/HTTP
Source0:	http://launchpad.net/apparmor/2.7/%{version}/+download/apparmor-%{version}.tar.gz
# Source0-md5:	2863e85bdfdf9ee35b83db6721fed1f1
URL:		http://apparmor.wiki.kernel.org/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	libapparmor-devel >= 1:%{version}
Requires:	apache(modules-api) = %apache_modules_api
Requires:	libapparmor >= 1:%{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_apparmor adds support to Apache 2 to provide AppArmor confinement
to individual CGI scripts handled by Apache modules like mod_php and
mod_perl. This package is part of a suite of tools that used to be
named SubDomain.

%description -l pl.UTF-8
mod_apparmor dodaje do Apache'a 2 obsługę ograniczeń AppArmor dla
poszczególnych skryptów CGI obsługiwanych przez moduły Apache'a takie
jak mod_php czy mod_perl. Ten pakiet jest częścią zestawu narzędzi
zwanych SubDomain.

%prep
%setup -q -n apparmor-%{version}

%build
%{__make} -C changehat/mod_apparmor mod_%{mod_name}.so \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT

cd changehat/mod_apparmor

install -D mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install -D mod_%{mod_name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/00_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/00_mod_apparmor.conf
%attr(755,root,root) %{_pkglibdir}/mod_apparmor.so
