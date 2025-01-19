FROM ubuntu:latest

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y cron openssh-server

RUN mkdir /var/run/sshd
RUN useradd -m -s /bin/bash user
RUN echo "user:password" | chpasswd

COPY motd /etc/motd
COPY crontab /etc/crontab
COPY apt-updater /usr/bin/apt-updater
COPY apt-updater.c /home/user/apt-updater.c
COPY flag.txt /flag.txt
COPY init.sh /init.sh

RUN chmod +x /init.sh
RUN chmod 400 /flag.txt
RUN chmod a+rx /usr/bin/apt-updater
RUN chmod u+s /usr/bin/apt-updater
RUN crontab -u user /etc/crontab

CMD /init.sh
