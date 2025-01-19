FROM pwn.red/jail

COPY --from=ubuntu:18.04@sha256:dca176c9663a7ba4c1f0e710986f5a25e672842963d95b960191e2d9f7185ebe / /srv

COPY ./flag.txt /srv/app/flag.txt
ADD ./doormat /srv/app/run

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run
