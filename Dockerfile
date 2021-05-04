FROM alpine


EXPOSE 53/TCP
EXPOSE 53/UDP

VOLUME /root

WORKDIR /root

COPY hosts /root/hosts

RUN apk --no-cache add dnsmasq

HEALTHCHECK CMD exit $(nslookup www.google.com localhost|grep -c "timed out")

ENTRYPOINT dnsmasq --bind-interfaces --cache-size=1500 --no-daemon --addn-hosts=/root/hosts
