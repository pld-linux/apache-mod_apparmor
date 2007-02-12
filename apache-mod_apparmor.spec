%define		mod_name	apparmor
%define 	apxs		/usr/sbin/apxs
%define		_ver 2.0
%define		_svnrel		64
Summary:	Apache module: AppArmor
Summary(pl.UTF-8):	Moduł Apache'a: AppArmor
Name:		apache-mod_%{mod_name}
Version:	%{_ver}.%{_svnrel}
Release:	0.9
License:	GPL
Group:		Networking/Daemons
Source0:	http://forgeftp.novell.com/apparmor/Development%20-%20October%20Snapshot/apache2-mod-%{mod_name}-%{_ver}-%{_svnrel}.tar.gz
# Source0-md5:	f01839ada8e1c2ea12d02384b89b15b5
URL:		http://forge.novell.com/modules/xfmod/project/?apparmor
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.0.52-2
BuildRequires:	libapparmor-devel
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)

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
%setup -q -n apache2-mod-%{mod_name}-%{_ver}

%build
%{__make} mod_%{mod_name}.so \
	APXS=%{apxs}

%install
rm -rf $RPM_BUILD_ROOT

install -D mod_%{mod_name}.so $RPM_BUILD_ROOT%{_pkglibdir}/mod_%{mod_name}.so
install -D mod_%{mod_name}.conf $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf/00_mod_%{mod_name}.conf

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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*.so
