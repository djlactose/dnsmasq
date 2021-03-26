FROM alpine


EXPOSE 53/TCP
EXPOSE 53/UDP

VOLUME /root

WORKDIR /root

COPY hosts /root/hosts

RUN apk add dnsmasq

HEALTHCHECK --interval=30s --timeout=60s --start-period=30s CMD exit $(nslookup www.google.com localhost|grep -c "timed out")

ENTRYPOINT dnsmasq --bind-interfaces --cache-size=1500 --no-daemon --addn-hosts=/root/hosts
