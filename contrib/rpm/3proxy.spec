%global contrib_dir %{_builddir}/%{name}-%{version}/contrib/rpm/
%define use_systemd (0%{?fedora} && 0%{?fedora} >= 18) || (0%{?rhel} && 0%{?rhel} >= 7) || (0%{?suse_version} == 1315)

Name:           3proxy
Version:        0.8.9
Release:        1%{?dist}

Summary:        Tiny but very powerful proxy
Summary(ru):    Маленький, но крайне мощный прокси-сервер

License:        BSD or ASL 2.0 or GPLv2+ or LGPLv2+
Group:          System Environment/Daemons
Url:            https://github.com/z3APA3A/3proxy

Source0:        https://github.com/z3APA3A/%{name}/archive/%{version}.tar.gz

BuildRequires:  openssl-devel

%if %{use_systemd}
BuildRequires:    systemd
Requires(post):   systemd
Requires(preun):  systemd
Requires(postun): systemd
%else
Requires(post):   systemd-sysv, systemd-units
Requires:         initscripts
%endif

%description
%{name} -- light proxy server.
Universal proxy server with HTTP, HTTPS, SOCKS v4, SOCKS v4a, SOCKS v5, FTP,
POP3, UDP and TCP portmapping, access control, bandwith control, traffic
limitation and accounting based on username, client IP, target IP, day time,
day of week, etc.

%description -l ru
%{name} -- маленький прокси сервер.
Это универсальное решение поддерживающее HTTP, HTTPS, SOCKS v4, SOCKS v4a,
SOCKS v5, FTP, POP3, UDP и TCP проброс портов (portmapping), списки доступа
управление скоростью доступа, ограничением трафика и статистикоу, базирующейся
на имени пользователя, слиентском IP адресе, IP цели, времени дня, дня недели
и т.д.

%prep
curl %{SOURCEURL0} -o %{_sourcedir}/%{SOURCE0}

%setup -n %{name}-%{version}
patch -p0  -s -b <  %{contrib_dir}/3proxy-0.6.1-config-path.patch
# To use "fedora" CFLAGS (exported)
sed -i -e "s/CFLAGS =/CFLAGS +=/" Makefile.Linux

%build
%{__make} -f Makefile.Linux

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_mandir}/man{3,8}
mkdir -p %{buildroot}%{_localstatedir}/log/%{name}
install -m755 -D src/%{name} %{buildroot}%{_bindir}/%{name}
install -m755 -D src/dighosts %{buildroot}%{_bindir}/dighosts
install -m755 -D src/ftppr %{buildroot}%{_bindir}/ftppr
install -m755 -D src/mycrypt %{buildroot}%{_bindir}/mycrypt
install -m755 -D src/pop3p %{buildroot}%{_bindir}/pop3p
install -m755 -D src/%{name} %{buildroot}%{_bindir}/%{name}
install -m755 -D src/proxy %{buildroot}%{_bindir}/htproxy
install -m755 -D src/socks %{buildroot}%{_bindir}/socks
install -m755 -D src/tcppm %{buildroot}%{_bindir}/tcppm
install -m755 -D src/udppm %{buildroot}%{_bindir}/udppm
install -pD -m644 cfg/3proxy.cfg.sample %{buildroot}/%{_sysconfdir}/%{name}.cfg

%if %{use_systemd}
install -pD -m755 %{contrib_dir}/%{name}.service %{buildroot}/%{_unitdir}/%{name}.service
%else
install -pD -m755 %{contrib_dir}/%{name}.init    %{buildroot}/%{_initrddir}/%{name}
%endif

for man in man/*.{3,8} ; do
    install "$man" "%{buildroot}%{_mandir}/man${man:(-1)}/"
done

%clean
rm -rf %{buildroot}

%post
%if %{use_systemd}
%systemd_post %{name}.service
%endif

%preun
%if %{use_systemd}
%systemd_preun %{name}.service
%endif

%postun
%if %{use_systemd}
%systemd_postun_with_restart %{name}.service
%endif

%files
%defattr(-,root,root,-)
%{_bindir}/*
%config(noreplace) %{_sysconfdir}/%{name}.cfg
%{_localstatedir}/log/%{name}
%doc README authors copying Release.notes
%{_mandir}/man8/*.8.gz
%{_mandir}/man3/*.3.gz

%if %{use_systemd}
%{_unitdir}/%{name}.service
%else
%{_initrddir}/%{name}
%endif

%changelog
* Fri Mar 17 2017 Anatolii Vorona <vorona.tolik@gmail.com> - 0.8.9
- upstream update
