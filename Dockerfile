FROM alpine

EXPOSE 53

VOLUME /root

WORKDIR /root

RUN apk add dnsmasq

ENTRYPOINT dnsmasq --bind-interfaces --cache-size=1500 --no-daemon --addn-hosts=/root/hosts
