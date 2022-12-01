echo "nameserver 8.8.8.8" > /etc/resolv.conf
echo "nameserver 1.1.1.1" >> /etc/resolv.conf
echo "nameserver 208.67.222.222" >> /etc/resolv.conf
echo "Added Name Servers"
if [[ "$Debug" == "false" ]]; then
    dnsmasq --bind-interfaces --cache-size=1500 -D -b -f --dns-forward-max=2048 --keep-in-foreground --log-queries --log-facility=LOCAL0 --addn-hosts=/root/data/hosts
else
    echo "Starting with debug on"
    dnsmasq --bind-interfaces --cache-size=1500 -D -b -f --dns-forward-max=2048 --keep-in-foreground --log-debug --log-queries --log-facility=LOCAL0 --addn-hosts=/root/data/hosts
fi