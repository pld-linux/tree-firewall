Summary:	Firewall building tool
Summary(pl):	Narzêdzie wspomagaj±ce budowanie firewalli
Name:		tree-firewall
Version:	0.1
Release:	1
Group:		Networking/Admin
License:	GPL
Vendor:		Olgierd Pieczul <wojrus@pld.org.pl>
Source0:	http://team.pld.org.pl/~wojrus/%{name}-%{version}.tar.gz
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Prereq:     /sbin/chkconfig
#Requires:	firewall-userspace-tool
Requires:   rc-scripts, tree
Conflicts:	firewall-init

%description
tree-firewall is a tool helping in building firewalls. It sets and
remove rule-sets. It can be also used as a SysV-init statup script.

%description -l pl
tree-firewall jest narzêdziem wspomagaj±cym budowanie firewalli.
Ustawia i usuwa zestawy regu³. Mo¿e byæ te¿ u¿ywany jako skrypt
startowy SysV.

%prep
%setup -q

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,firewall,rc.d/init.d},%{_sbindir},%{_datadir}/%{name}}
install firewall $RPM_BUILD_ROOT%{_sbindir}/
install functions-* $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s %{_sbindir}/firewall $RPM_BUILD_ROOT/etc/rc.d/init.d/firewall
echo "#USERSPACE_TOOL=" > $RPM_BUILD_ROOT/etc/sysconfig/firewall
gzip -9nf README ChangeLog

%post
/sbin/chkconfig --add firewall

%preun
if [ "$1" = "0" ]; then
    /sbin/chkconfig --del firewall
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README.gz ChangeLog.gz
%dir %{_sysconfdir}/firewall
%attr(755,root,root) %{_sbindir}/firewall
%attr(755,root,root) %{_datadir}/%{name}
%attr(750,root,root) /etc/rc.d/init.d/firewall
%attr(700,root,root) %verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall
