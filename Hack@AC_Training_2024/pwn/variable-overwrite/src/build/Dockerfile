FROM pwn.red/jail

COPY --from=ubuntu:20.04@sha256:bb1c41682308d7040f74d103022816d41c50d7b0c89e9d706a74b4e548636e54 / /srv

COPY ./flag.txt /srv/app/flag.txt
COPY ./chall /srv/app/run

RUN chmod 444 /srv/app/flag.txt
RUN chmod +x /srv/app/run
