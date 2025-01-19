FROM debian:10

RUN mkdir /app
COPY flag.txt /root

RUN apt-get update
RUN apt-get install sudo socat netcat-traditional python3 build-essential -y
RUN useradd -m user
RUN echo 'user:password' | chpasswd

COPY checkflag.c /root
RUN gcc -o /home/user/checkflag /root/checkflag.c
RUN /bin/chmod a+rwx /home/user/checkflag
RUN /bin/chmod u+s /home/user/checkflag

RUN find /bin -type l ! -name sh -delete
RUN find /usr/bin -type l ! -name python3 -delete
RUN /bin/chmod go-rwx /usr/bin/*
RUN /bin/chmod go-rwx /bin/*
RUN /bin/chmod a+x /bin/dash
RUN /bin/chmod a+x /bin/echo
RUN /bin/chmod a+x /bin/chmod
RUN /bin/chmod a+x /usr/bin/sudo
RUN /bin/chmod a+x /usr/bin/base64
RUN /bin/chmod a+x /usr/bin/sha256sum
RUN /bin/chmod a+x /bin/nc.traditional
RUN /bin/chmod a+x /usr/bin/socat
RUN ln -sf /bin/nc.traditional /bin/nc
RUN ln -sf /bin/nc.traditional /bin/netcat
#RUN which nc
RUN /bin/chmod a+x /bin/tar
RUN /bin/chmod a+x /usr/bin/python3


WORKDIR /home/user
USER user

EXPOSE 9999

CMD ["socat", "-t", "3600", "tcp-listen:9999,reuseaddr,fork", "system:/bin/dash"]
