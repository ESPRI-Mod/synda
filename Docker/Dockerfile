FROM centos:centos6

RUN yum install -y gcc python python-pip python-devel openssl-devel sqlite sqlite-devel libxslt-devel libxml2-devel zlib-devel libffi-devel wget bc which tar

RUN useradd synda

ENV ST_HOME=/home/synda/sdt
ENV PATH=$ST_HOME/bin:$PATH

RUN su synda -c "mkdir -p /home/synda/src/synda && cd /home/synda/src/synda && wget https://raw.githubusercontent.com/Prodiguer/synda/master/sdc/install.sh && chmod +x install.sh && ./install.sh"

RUN wget -O /tmp/synda_autologin.sh https://raw.githubusercontent.com/Prodiguer/synda/master/Docker/synda_autologin.sh; cat /tmp/synda_autologin.sh >> /root/.bashrc

RUN su synda -c "echo 'export ST_HOME=/home/synda/sdt' >> /home/synda/.bashrc; echo 'export PATH=$ST_HOME/bin:$PATH' >> /home/synda/.bashrc"
