FROM pwn.red/jail

COPY --from=ubuntu:16.04@sha256:1f1a2d56de1d604801a9671f301190704c25d604a416f59e03c04f5c6ffee0d6 / /srv

COPY ./flag.txt /srv/app/flag.txt
ADD ./ret2win /srv/app/run

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run
