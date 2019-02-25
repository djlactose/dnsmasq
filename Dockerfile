FROM alpine

EXPOSE 53

VOLUME /root

WORKDIR /root

COPY hosts /root/hosts

RUN apk add dnsmasq 

ENTRYPOINT dnsmasq --bind-interfaces --cache-size=1500 --no-daemon --addn-hosts=/root/hosts
