FROM alpine

EXPOSE 53/TCP
EXPOSE 53/UDP
EXPOSE 8000

ENV Debug=false

VOLUME /etc/dnsmasq.d/

WORKDIR /etc/dnsmasq.d/

COPY hosts /etc/dnsmasq.d/hosts
COPY run.sh /root/bin/run.sh
COPY app.py /root/web/app.py
COPY templates/index.html /root/web/templates/index.html

RUN apk --no-cache add py3-flask py3-gunicorn dnsmasq && \
chmod 700 /root/bin/run.sh

HEALTHCHECK CMD exit $(nslookup localhost localhost|grep -c "timed out")

ENTRYPOINT /root/bin/run.sh