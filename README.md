# DNS MASQ

This container makes it easy to manage a DNS server within your container environment.

## Persistent Storage
* /etc/dnsmasq.d/hosts - this is where the dns entries will be stored

## Ports

* 53/TCP - This is sometimes user in environments when UDP is not able to be utilized or is blocked
* 53/UDP - This is the standard DNS port
* 8000 - This is for the web admin interface