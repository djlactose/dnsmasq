FROM alpine

EXPOSE 53/TCP
EXPOSE 53/UDP
EXPOSE 8000

ENV Debug=false

VOLUME /etc/dnsmasq.d/

WORKDIR /etc/dnsmasq.d/

COPY run.sh /root/bin/run.sh
COPY app.py /root/web/app.py
COPY templates/ /root/web/templates/

RUN apk --no-cache add py3-passlib py3-flask py3-gunicorn py3-flask-sqlalchemy dnsmasq && \
chmod 700 /root/bin/run.sh && \
touch /etc/dnsmasq.d/hosts

HEALTHCHECK CMD exit $(nslookup localhost localhost|grep -c "timed out")

ENTRYPOINT /root/bin/run.sh