FROM alpine

ENV Lookup_DNS=8.8.8.8

EXPOSE 53/TCP
EXPOSE 53/UDP

VOLUME /root

WORKDIR /root

COPY hosts /root/hosts
COPY run.sh /root/bin/run.sh

RUN apk add dnsmasq 

#ENTRYPOINT dnsmasq --bind-interfaces --cache-size=1500 --no-daemon --addn-hosts=/root/hosts
ENTRYPOINT /root/bin/run.sh
