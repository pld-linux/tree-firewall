Summary:	Firewall building tool
Summary(pl):	Narzêdzie wspomagaj±ce budowanie firewalli
Name:		tree-firewall
Version:	0.2
Release:	1
Epoch:		1
License:	GPL
Group:		Networking/Admin
Vendor:		Olgierd Pieczul <wojrus@pld.org.pl>
Source0:	ftp://ftp.pld.org.pl/people/wojrus/tree-firewall/%{name}-%{version}.tar.gz
Prereq:		/sbin/chkconfig
#Requires:	firewall-userspace-tool
Requires:	rc-scripts, tree
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Conflicts:	firewall-init

%define		_sbindir	/sbin

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
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,firewall,rc.d/init.d},%{_sbindir},%{_datadir}/%{name},/tmp/tree-firewall,%{_mandir}/man8}

install firewall $RPM_BUILD_ROOT/etc/rc.d/init.d/firewall
install functions-* $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /etc/rc.d/init.d/firewall $RPM_BUILD_ROOT%{_sbindir}/rc.firewall

echo "# tree-firewall config file" > $RPM_BUILD_ROOT/etc/sysconfig/firewall
install firewall.8 $RPM_BUILD_ROOT%{_mandir}/man8
echo ".so firewall.8" > $RPM_BUILD_ROOT%{_mandir}/man8/rc.firewall.8

%post
echo -n "Trying to identify which userspace tool do you use... "
echo -ne "\n#USERSPACE_TOOL=" >> /etc/sysconfig/firewall
if [ -f /usr/sbin/iptables -o -f /sbin/iptables ]; then
	echo "iptables"
	echo "iptables" >> /etc/sysconfig/firewall
elif [ -f /sbin/ipchains -o -f /usr/sbin/ipchains ]; then
	echo "ipchains"
	echo "ipchains" >> /etc/sysconfig/firewall
else
	echo "failed!"
	echo "unknown" >> /etc/sysconfig/firewall
fi
echo "You should modify /etc/sysconfig/firewall"

/sbin/chkconfig --add firewall

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del firewall
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,750)
%doc README ChangeLog
%dir %{_sysconfdir}/firewall
%dir /tmp/tree-firewall
%attr(755,root,root) %{_sbindir}/rc.firewall
%attr(755,root,root) %{_datadir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/firewall
%attr(640,root,root) %verify(not size mtime md5) %config(noreplace) /etc/sysconfig/firewall
%{_mandir}/man8/*
