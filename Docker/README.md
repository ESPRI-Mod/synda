Usage
===

 1/ Installation and startup
---

```
[user@host~]$ mkdir -p /tmp/synda/sdt/conf; wget -O /tmp/synda/sdt/conf/sdt.conf https://github.com/Prodiguer/synda/raw/master/sdt/conf/sdt.conf
[user@host~]$ sudo docker pull ncaripsl/synda
```

2/ OpenID/Password configuration
---

```
[user@host~]$ vi /tmp/synda/sdt/conf/sdt.conf
```

3/ Startup container in daemon mode and mount host directories as container data volumes owned by your host user and group
---

```
[user@host~]$ sudo docker run -d -t -i -name my_synda -v /tmp/synda/sdt/data/:/home/synda/sdt/data/ -v /tmp/synda/sdt/db/:/home/synda/sdt/db/ -v /tmp/synda/sdt/log/:/home/synda/sdt/log/ -v /tmp/synda/sdt/selection:/home/synda/sdt/selection/ -v /tmp/synda/sdt/conf/:/home/synda/sdt/conf/ -e UID=$UID -e GID=$GROUPS ncaripsl/synda /bin/bash
```

4/ Dataset installation and download
---

```
[user@host~]$ sudo docker ps
[user@host~]$ sudo docker attach my_synda
[synda@204fcee0d7e5 ~]$ synda install [dataset_name]
[synda@204fcee0d7e5 ~]$ synda daemon start &
```

5/ Container detachment
---

```
[synda@204fcee0d7e5 ~]$ Ctrl+p+Ctrl+q
```

6/ Listing retrieved data, logs, db, selection and config on host directories
---

```
[user@host~]$ ls /tmp/synda/sdt/data/
[user@host~]$ ls /tmp/synda/sdt/log/
[user@host~]$ ls /tmp/synda/sdt/db/
[user@host~]$ ls /tmp/synda/sdt/selection/
[user@host~]$ ls /tmp/synda/sdt/conf/
```
