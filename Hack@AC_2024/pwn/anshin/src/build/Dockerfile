FROM pwn.red/jail

COPY --from=ubuntu:22.04@sha256:2b7412e6465c3c7fc5bb21d3e6f1917c167358449fecac8176c6e496e5c1f05f / /srv

COPY ./flag.txt /srv/app/flag.txt
COPY ./anshin-impact /srv/app/run

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run
