echo "nameserver	$Lookup_DNS" >> /etc/resolv.conf
dnsmasq --bind-interfaces --cache-size=1500 --no-daemon --addn-hosts=/root/hosts
