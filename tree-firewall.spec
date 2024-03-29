Summary:	Firewall building tool
Summary(pl.UTF-8):	Narzędzie wspomagające budowanie firewalli
Name:		tree-firewall
Version:	0.2
Release:	5
Epoch:		1
License:	GPL
Group:		Networking/Admin
Source0:	ftp://ftp.pld.org.pl/people/wojrus/tree-firewall/%{name}-%{version}.tar.gz
# Source0-md5:	101385c143c0b45ec8c35bc4eae0bbea
Patch0:		%{name}-raw.patch
Requires(post):	grep
Requires(post,preun):	/sbin/chkconfig
#Requires:	firewall-userspace-tool
Requires:	rc-scripts
Requires:	tree
Conflicts:	firewall-init
Conflicts:	shorewall
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
tree-firewall is a tool helping in building firewalls. It sets and
remove rule-sets. It can be also used as a SysV-init startup script.

%description -l pl.UTF-8
tree-firewall jest narzędziem wspomagającym budowanie firewalli.
Ustawia i usuwa zestawy reguł. Może być też używany jako skrypt
startowy SysV.

%prep
%setup -q
%patch0 -p1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,firewall,rc.d/init.d},%{_sbindir},%{_datadir}/%{name},/tmp/tree-firewall,%{_mandir}/man8}

install firewall $RPM_BUILD_ROOT/etc/rc.d/init.d/firewall
install functions-* $RPM_BUILD_ROOT%{_datadir}/%{name}
ln -s /etc/rc.d/init.d/firewall $RPM_BUILD_ROOT%{_sbindir}/rc.firewall

echo "# tree-firewall config file" > $RPM_BUILD_ROOT/etc/sysconfig/firewall
install firewall.8 $RPM_BUILD_ROOT%{_mandir}/man8
echo ".so firewall.8" > $RPM_BUILD_ROOT%{_mandir}/man8/rc.firewall.8

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q '#\?USERSPACE_TOOL' /etc/sysconfig/firewall ; then
	echo -n "Trying to identify which userspace tool do you use... "
	if [ -f /usr/sbin/iptables -o -f /sbin/iptables ]; then
		echo "iptables"
		echo -e "\n#USERSPACE_TOOL=iptables" >> /etc/sysconfig/firewall
	elif [ -f /sbin/ipchains -o -f /usr/sbin/ipchains ]; then
		echo "ipchains"
		echo -e "\n#USERSPACE_TOOL=ipchains" >> /etc/sysconfig/firewall
	else
		echo "failed!"
		echo -e "\n#USERSPACE_TOOL=unknown" >> /etc/sysconfig/firewall
	fi
	echo "You should modify /etc/sysconfig/firewall"
fi
/sbin/chkconfig --add firewall

%preun
if [ "$1" = "0" ]; then
	/sbin/chkconfig --del firewall
fi

%files
%defattr(644,root,root,755)
%doc README ChangeLog
%defattr(644,root,root,750)
%dir %{_sysconfdir}/firewall
# huh? will be removed by rc.sysinit
%dir /tmp/tree-firewall
%attr(755,root,root) %{_sbindir}/rc.firewall
%attr(755,root,root) %{_datadir}/%{name}
%attr(754,root,root) /etc/rc.d/init.d/firewall
%attr(640,root,root) %verify(not md5 mtime size) %config(noreplace) /etc/sysconfig/firewall
%{_mandir}/man8/*
