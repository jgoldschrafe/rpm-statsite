Name:             statsite
Version:          0
Release:          0.5.0
Summary:          Stats aggregation server
Group:            Applications/Internet
License:          BSD
URL:              https://github.com/armon/statsite
Source:           https://github.com/armon/statsite/archive/v%{release}.tar.gz
Source1:          statsite.conf.default
Source2:          statsite.init
BuildRoot:        %{_tmppath}/%{name}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    check
BuildRequires:    scons


%description
This is a stats aggregation server. Statsite is based heavily on Etsy's StatsD 
https://github.com/etsy/statsd. This is a re-implementation of the Python 
version of statsite.


%prep
%setup -q -n%{name}-%{release}


%build
scons


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/statsite
install -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/statsite/statsite.conf

install -d %{buildroot}%{_initrddir}
install -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/statsite

install -d %{buildroot}%{_bindir}
install -m 0755 statsite %{buildroot}%{_bindir}/

install -d %{buildroot}%{_prefix}/lib/statsite/sinks
install sinks/graphite.py %{buildroot}%{_prefix}/lib/statsite/sinks/

install -d %{buildroot}%{_localstatedir}/run/statsite


%check
# Tests appear to be broken currently
#scons test_runner


%clean
rm -rf %{buildroot}


%pre
getent group statsite >/dev/null || groupadd statsite
getent passwd statsite >/dev/null || \
    useradd -r -g statsite -d '/etc/statsite' -s /sbin/nologin \
    -c "Statsite Service User" statsite


%post
/sbin/chkconfig --add statsite


%preun
if [ $1 -eq 0 ]; then
    /sbin/service statsite stop 2>&1
    /sbin/chkconfig --del statsite
fi


%postun
if [ $1 -ge 1 ]; then
    /sbin/service statsite condrestart 2>&1 || :
fi


%files
%doc LICENSE README.md
%defattr(-,root,root,-)
%{_bindir}/statsite
%{_prefix}/lib/statsite/
%dir %{_sysconfdir}/statsite/
%config(noreplace) %{_sysconfdir}/statsite/statsite.conf
%{_initrddir}/statsite
%attr(0755,statsite,statsite) %{_localstatedir}/run/statsite/


%changelog
* Mon Jul 16 2012 Jeff Goldschrafe <jeff@holyhandgrenade.org> - 0-0.20120716gitea1efe3
- Initial package
