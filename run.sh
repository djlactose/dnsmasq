gunicorn -w 2 -b 0.0.0.0:8000 --daemon --chdir /root/web/ app:app
if [[ "$Debug" == "false" ]]; then
    dnsmasq --bind-interfaces --no-hosts --cache-size=1500 -q -D -b -f --dns-forward-max=2048 --keep-in-foreground --log-queries --log-facility=LOCAL0 --addn-hosts=/etc/dnsmasq.d/hosts
else
    echo "Starting with debug on"
    dnsmasq --bind-interfaces --no-hosts --cache-size=1500 -q -D -b -f --dns-forward-max=2048 --keep-in-foreground --log-debug --log-queries --log-facility=LOCAL0 --addn-hosts=/etc/dnsmasq.d/hosts
fi